"""Score items with Laya into data/labels/item_features.csv (CONTRACT.md file 2), write the
hand-label sheet, and compute data/labels/agreement.json (file 9).

Usage, from the project root (Laya needs a GPU; run on a Colab T4):
    python src/score.py --smoke                    score 50 stratified items, print answers and speed
    python src/score.py --smoke --items data/clean/MOCK_items.csv
    python src/score.py                            full run on data/clean/items.csv (resumable)
    python src/score.py --sample 0.5               full run on a fixed 50% subsample
    python src/score.py --provider fallback        same questions through the Claude API
    python src/score.py --handlabel                write data/labels/handlabel_50.csv (never overwrites)
    python src/score.py --agreement                write data/labels/agreement.json

The questions are frozen (CONTRACT.md file 2, CONTEXT.md section 7). Do not reword them.
The fallback provider reads ANTHROPIC_API_KEY from the environment or from .env.
Owner: P2. Python 3.10+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "clean" / "items.csv"
FEATURES = ROOT / "data" / "labels" / "item_features.csv"
CHECKPOINT = ROOT / "data" / "labels" / "checkpoint.jsonl"   # gitignored
RAW = ROOT / "data" / "labels" / "laya_raw.jsonl"              # gitignored
HANDLABEL = ROOT / "data" / "labels" / "handlabel_50.csv"
AGREEMENT = ROOT / "data" / "labels" / "agreement.json"

LAYA_CHECKPOINT = "convaiinnovations/laya"
LAYA_REVISION = "55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851"
FALLBACK_MODEL = "claude-opus-5-5"
CHECKPOINT_EVERY = 500

BANNERS = ["dicks", "house_of_sport", "golf_galaxy", "foot_locker", "other"]
AUTHORS = ["customer", "employee", "other"]
TOPICS = ["availability", "price_promo", "service_staff", "fulfillment_returns",
          "product_quality", "store_experience", "other"]
INTENTS = ["up", "flat", "down"]
CHOICE_OPTIONS = {"banner": BANNERS, "author": AUTHORS, "topic": TOPICS, "intent": INTENTS}

FEATURE_COLUMNS = (["item_id", "p_relevant"] + [f"p_banner_{b}" for b in BANNERS]
                   + [f"p_author_{a}" for a in AUTHORS] + [f"p_topic_{t}" for t in TOPICS]
                   + ["p_stockout"] + [f"p_intent_{x}" for x in INTENTS]
                   + ["promo_score_exp", "promo_entropy", "model_version", "scored_at"])

# ---------------------------------------------------------------- frozen questions

STATE_TEMPLATE = ("Source: {source}. Location/community: {banner_hint}. Company context: Dick's "
                  "Sporting Goods (DKS) operates Dick's Sporting Goods, House of Sport, Golf Galaxy, "
                  "and Foot Locker stores. Text: {text}")

QUESTIONS = {
    "relevant": {
        "type": "noul",
        "instructions": "Does this text describe a first-hand experience or observation about "
                        "shopping at, buying from, or working at Dick's Sporting Goods, House of "
                        "Sport, Golf Galaxy, or Foot Locker?"},
    "banner": {
        "type": "choice",
        "instructions": "Which store or retailer is this text about?",
        "criteria": {"dicks": "Dick's Sporting Goods store or website",
                     "house_of_sport": "a House of Sport store",
                     "golf_galaxy": "Golf Galaxy",
                     "foot_locker": "Foot Locker",
                     "other": "another retailer or unclear"}},
    "author": {
        "type": "choice",
        "instructions": "Who wrote this text?",
        "criteria": {"customer": "a shopper or customer",
                     "employee": "a current or former employee",
                     "other": "neither, or unclear"}},
    "topic": {
        "type": "choice",
        "instructions": "What is the main subject of this text?",
        "criteria": {"availability": "products, sizes, or items unavailable or hard to find",
                     "price_promo": "prices, sales, discounts, coupons, markdowns",
                     "service_staff": "staffing levels, help, wait times, employee behavior",
                     "fulfillment_returns": "online orders, store pickup, shipping, returns",
                     "product_quality": "quality of products bought",
                     "store_experience": "store layout, cleanliness, events, in-store features",
                     "other": "anything else"}},
    "stockout": {
        "type": "noul",
        "instructions": "Does the text report that a product, size, or item the author wanted "
                        "was unavailable or out of stock?"},
    "intent": {
        "type": "choice",
        "instructions": "How does this experience change whether the author will shop here again?",
        "criteria": {"up": "the experience makes the author more likely to shop here again",
                     "flat": "no change, or not stated",
                     "down": "the experience makes the author less likely to shop here again"}},
    "promo": {
        "type": "score",
        "instructions": "How much did discounts drive the purchase or visit?",
        "criteria": ["discounts not mentioned or irrelevant",
                     "discounts mentioned in passing",
                     "discounts were one reason among several",
                     "discounts were the main reason",
                     "the purchase or visit happened only because of a discount"]},
}


def rel(path: Path) -> str:
    """A path relative to the project root when it is inside it."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def build_state(row) -> str:
    hint = "" if pd.isna(row.banner_hint) else str(row.banner_hint)
    return STATE_TEMPLATE.format(source=row.source, banner_hint=hint, text=row.text)


# ---------------------------------------------------------------- answers -> features

def normalized(values: list[float]) -> np.ndarray:
    """Clip to [0, 1] and rescale to sum to 1 (Laya rounds each probability to 4 decimals)."""
    p = np.clip(np.array(values, dtype=float), 0, 1)
    total = p.sum()
    return p / total if total > 0 else np.full(len(p), 1 / len(p))


def features_from_answers(item_id: str, ans: dict, model_version: str, scored_at: str) -> dict:
    """One item_features.csv row from Laya-shaped answers (CONTRACT.md file 2)."""
    row = {"item_id": item_id, "p_relevant": float(ans["relevant"]["noul"]),
           "p_stockout": float(ans["stockout"]["noul"])}
    for q, options in CHOICE_OPTIONS.items():
        probs = ans[q]["probabilities"]
        row.update(zip([f"p_{q}_{o}" for o in options], normalized([probs[o] for o in options])))
    promo = normalized([ans["promo"]["probabilities"][str(i)] for i in range(5)])
    nz = promo[promo > 0]
    row["promo_score_exp"] = float((np.arange(1, 6) * promo).sum())  # levels 1..5, not Laya's 0..4
    row["promo_entropy"] = float(-(nz * np.log(nz)).sum())
    row["model_version"], row["scored_at"] = model_version, scored_at
    return row


# ---------------------------------------------------------------- providers

class LayaProvider:
    """Laya on a fixed checkpoint and revision. Deterministic for a fixed batch composition."""

    name = "laya"

    def __init__(self, batch_size: int):
        import laya
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if device == "cpu":
            print("WARNING: no GPU found; Laya will run on CPU and be slow.")
        self.agent = laya.load(LAYA_CHECKPOINT, device=device, revision=LAYA_REVISION)
        self.batch_size = batch_size
        self.model_version = f"laya {laya.__version__} {LAYA_CHECKPOINT}@{LAYA_REVISION[:8]}"

    def score(self, states: list[str]) -> list[tuple[dict | None, str]]:
        results = self.agent.predict_batch(states, QUESTIONS, batch_size=self.batch_size)
        return [(r.get("answers", r), self.model_version) for r in results]


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Put KEY=VALUE lines from .env into the environment (existing variables win)."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


class ClaudeProvider:
    """Fallback: the same frozen questions through the Claude API, returning Laya-shaped answers.

    Structured output (a JSON schema) guarantees parseable answers. The server-side refusal
    fallback is on, so a declined request is retried on another model inside the same call;
    the model that actually answered is recorded in model_version.
    """

    name = "fallback"

    def __init__(self, model: str, workers: int):
        import anthropic
        load_dotenv()
        self.client = anthropic.Anthropic(max_retries=6)  # SDK backs off on 429 and 5xx
        self.model, self.workers = model, workers
        self.system = self._system_prompt()
        self.schema = self._schema()

    @staticmethod
    def _system_prompt() -> str:
        lines = ["You estimate probabilities for fixed questions about one text item. For each "
                 "yes/no question, give the probability that the answer is yes. For each "
                 "multiple-choice or scale question, give a probability for every option; the "
                 "probabilities for one question must sum to 1. Answer from the text alone.", ""]
        for qid, q in QUESTIONS.items():
            lines.append(f"{qid}: {q['instructions']}")
            if q["type"] == "choice":
                lines += [f"  {k} = {v}" for k, v in q["criteria"].items()]
            elif q["type"] == "score":
                lines += [f"  {i} = {v}" for i, v in enumerate(q["criteria"], start=1)]
        return "\n".join(lines)

    @staticmethod
    def _schema() -> dict:
        def probs(keys: list[str]) -> dict:
            return {"type": "object", "properties": {k: {"type": "number"} for k in keys},
                    "required": keys, "additionalProperties": False}
        props = {"relevant": {"type": "number"}, "stockout": {"type": "number"},
                 "promo": probs([str(i) for i in range(1, 6)])}
        props.update({q: probs(options) for q, options in CHOICE_OPTIONS.items()})
        return {"type": "object", "properties": props, "required": list(props),
                "additionalProperties": False}

    def _one(self, state: str) -> tuple[dict | None, str]:
        import anthropic
        try:
            resp = self.client.beta.messages.create(
                model=self.model,
                max_tokens=4000,
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
                system=[{"type": "text", "text": self.system, "cache_control": {"type": "ephemeral"}}],
                output_config={"effort": "low",
                               "format": {"type": "json_schema", "schema": self.schema}},
                messages=[{"role": "user", "content": state}],
            )
        except (anthropic.BadRequestError, anthropic.APIStatusError, anthropic.APIConnectionError) as exc:
            print(f"WARNING: API call failed ({type(exc).__name__}); item left unscored.")
            return None, f"fallback:{self.model}"
        if resp.stop_reason in ("refusal", "max_tokens"):
            print(f"WARNING: stop_reason={resp.stop_reason}; item left unscored.")
            return None, f"fallback:{resp.model}"
        data = json.loads(next(b.text for b in resp.content if b.type == "text"))
        answers = {"relevant": {"noul": data["relevant"]}, "stockout": {"noul": data["stockout"]},
                   "promo": {"probabilities": {str(i - 1): data["promo"][str(i)] for i in range(1, 6)}}}
        answers.update({q: {"probabilities": data[q]} for q in CHOICE_OPTIONS})
        return answers, f"fallback:{resp.model}"

    def score(self, states: list[str]) -> list[tuple[dict | None, str]]:
        with ThreadPoolExecutor(self.workers) as pool:
            return list(pool.map(self._one, states))


def make_provider(args):
    if args.provider == "laya":
        return LayaProvider(args.batch_size)
    return ClaudeProvider(args.fallback_model, args.workers)


# ---------------------------------------------------------------- sampling

def stable_hash(text: str, salt: str = "") -> int:
    return int(hashlib.sha256((salt + text).encode("utf-8")).hexdigest()[:12], 16)


def subsample(items: pd.DataFrame, frac: float) -> pd.DataFrame:
    """A fixed subsample: the same items every run, whatever the order of the input."""
    keep = items.item_id.map(lambda i: stable_hash(i, "subsample") % 10_000 < frac * 10_000)
    return items[keep]


def stratified(items: pd.DataFrame, n: int, salt: str) -> pd.DataFrame:
    """n items spread evenly over source x year of date_low, in a fixed pseudo-random order."""
    df = items.assign(_year=items.date_low.str[:4],
                      _h=items.item_id.map(lambda i: stable_hash(i, salt)))
    groups = [g.sort_values("_h") for _, g in df.groupby(["source", "_year"])]
    picked, k = [], 0
    while len(picked) < min(n, len(df)):
        for g in groups:
            if k < len(g) and len(picked) < n:
                picked.append(g.iloc[k])
        k += 1
    return pd.DataFrame(picked).drop(columns=["_year", "_h"])


# ---------------------------------------------------------------- scoring runs

def read_items(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, keep_default_na=False, na_values=[""],
                       dtype={"item_id": str, "text": str, "banner_hint": str})


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_checkpoint(provider_name: str) -> dict[str, dict]:
    done = {}
    if CHECKPOINT.exists():
        for line in CHECKPOINT.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec["provider"] != provider_name:
                sys.exit(f"Checkpoint was made with provider '{rec['provider']}'. Mixing providers "
                         "in one run is a new variant; move the checkpoint aside to start over.")
            done[rec["row"]["item_id"]] = rec["row"]
    return done


def score_items(items: pd.DataFrame, provider, batch_size: int) -> pd.DataFrame:
    """Score every item not already in the checkpoint; resumable. Returns all scored rows."""
    done = load_checkpoint(provider.name)
    todo = items[~items.item_id.isin(done)].sort_values("item_id")
    print(f"{len(done)} items already scored; {len(todo)} to go.")
    pending, failed, t0 = [], 0, time.time()
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    with RAW.open("a", encoding="utf-8") as raw, CHECKPOINT.open("a", encoding="utf-8") as ckpt:
        for start in range(0, len(todo), batch_size):
            chunk = todo.iloc[start:start + batch_size]
            results = provider.score([build_state(r) for r in chunk.itertuples()])
            stamp = now_iso()
            for item_id, (ans, version) in zip(chunk.item_id, results):
                if ans is None:
                    failed += 1
                    continue
                raw.write(json.dumps({"item_id": item_id, "provider": provider.name,
                                      "model_version": version, "answers": ans}) + "\n")
                row = features_from_answers(item_id, ans, version, stamp)
                done[item_id] = row
                pending.append(row)
            raw.flush()
            last = start + batch_size >= len(todo)
            if len(pending) >= CHECKPOINT_EVERY or last:
                for row in pending:
                    ckpt.write(json.dumps({"provider": provider.name, "row": row}) + "\n")
                ckpt.flush()
                pending = []
                n = min(start + batch_size, len(todo))
                rate = n / max(time.time() - t0, 1e-9)
                eta = (len(todo) - n) / rate / 60 if rate else float("nan")
                print(f"  checkpoint: {n}/{len(todo)} this run, {rate:.1f} items/s, "
                      f"about {eta:.0f} min left")
    if failed:
        print(f"WARNING: {failed} items failed and stay unscored; rerun to retry them.")
    rows = [done[i] for i in items.item_id if i in done]
    return pd.DataFrame(rows, columns=FEATURE_COLUMNS)


def smoke(items: pd.DataFrame, provider, batch_size: int) -> None:
    """Score 50 stratified items without writing any file; print answers and speed."""
    sample = stratified(items, 50, salt="smoke")
    t0 = time.time()
    results = []
    for start in range(0, len(sample), batch_size):
        chunk = sample.iloc[start:start + batch_size]
        results += provider.score([build_state(r) for r in chunk.itertuples()])
    seconds = time.time() - t0
    ok = 0
    for row, (ans, version) in zip(sample.itertuples(), results):
        if ans is None:
            print(f"{row.item_id}  FAILED")
            continue
        ok += 1
        f = features_from_answers(row.item_id, ans, version, now_iso())
        top = {q: max(options, key=lambda o: f[f"p_{q}_{o}"]) for q, options in CHOICE_OPTIONS.items()}
        snippet = " ".join(str(row.text).split())[:70]
        print(f"{row.item_id}  {row.source:6} {str(row.date_low)[:4]}  rel={f['p_relevant']:.2f} "
              f"banner={top['banner']:<14} author={top['author']:<8} topic={top['topic']:<19} "
              f"stockout={f['p_stockout']:.2f} intent={top['intent']:<4} "
              f"promo={f['promo_score_exp']:.1f}  | {snippet}")
    rate = len(sample) / seconds if seconds else float("nan")
    print(f"\n{ok}/{len(sample)} items scored in {seconds:.1f} s: {rate:.2f} items/s "
          "(includes warm-up, so a full run is usually faster).")
    if ITEMS.exists():
        n_full = len(read_items(ITEMS))
        print(f"Full run estimate for {n_full} items in data/clean/items.csv: "
              f"{n_full / rate / 60:.0f} min. Gate at 8:30: subsample with --sample if over 40 min.")


# ---------------------------------------------------------------- hand labels and agreement

YES, NO = {"yes", "y", "1", "true"}, {"no", "n", "0", "false"}


def write_handlabel(items: pd.DataFrame) -> None:
    if HANDLABEL.exists():
        sys.exit(f"{rel(HANDLABEL)} exists and may hold hand labels; not overwriting.")
    sheet = stratified(items, 50, salt="handlabel")[["item_id", "text"]]
    for col in ["relevant", "topic", "stockout", "intent"]:
        sheet[col] = ""
    sheet.to_csv(HANDLABEL, index=False, lineterminator="\n")
    print(f"Wrote {rel(HANDLABEL)}. Fill relevant and stockout with yes/no, topic with "
          f"one of {TOPICS}, intent with one of {INTENTS}. Leave a cell empty to skip it.")


def cohen_kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)


def laya_label(row: pd.Series, question: str) -> str:
    if question in ("relevant", "stockout"):
        return "yes" if row[f"p_{question}"] >= 0.5 else "no"
    options = CHOICE_OPTIONS[question]
    return max(options, key=lambda o: row[f"p_{question}_{o}"])


def human_label(value, question: str) -> str:
    v = str(value).strip().lower()
    if question in ("relevant", "stockout"):
        return "yes" if v in YES else "no" if v in NO else ""
    return v if v in CHOICE_OPTIONS[question] else ""


def write_agreement() -> None:
    labels = pd.read_csv(HANDLABEL, dtype=str, keep_default_na=False)
    feats = pd.read_csv(FEATURES, keep_default_na=False, na_values=[""], dtype={"item_id": str})
    merged = labels.merge(feats, on="item_id", how="inner")
    questions = []
    for q in ["relevant", "topic", "stockout", "intent"]:
        human = merged[q].map(lambda v: human_label(v, q))
        bad = (merged[q].str.strip() != "") & (human == "")
        if bad.any():
            print(f"WARNING: {int(bad.sum())} {q} labels not understood and skipped, e.g. "
                  f"{merged.loc[bad, q].iloc[0]!r}")
        use = merged[human != ""]
        h, m = list(human[human != ""]), [laya_label(r, q) for _, r in use.iterrows()]
        kappa = cohen_kappa(h, m)
        questions.append({"question": q, "n": len(h),
                          "pct_agreement": round(100 * sum(x == y for x, y in zip(h, m)) / len(h), 1)
                          if h else 0.0,
                          "cohen_kappa": None if kappa is None else round(kappa, 3)})
    versions = merged.model_version.value_counts()
    out = {"n_items": len(labels),
           "model_version": versions.index[0] if len(versions) else "unknown",
           "questions": questions}
    AGREEMENT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for q in questions:
        print(f"{q['question']:9} n={q['n']:3} agreement={q['pct_agreement']:5.1f}%  kappa={q['cohen_kappa']}")
    print(f"Wrote {rel(AGREEMENT)}.")


# ---------------------------------------------------------------- command line

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score items with Laya (CONTRACT.md file 2).")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--smoke", action="store_true", help="score 50 stratified items; write nothing")
    mode.add_argument("--handlabel", action="store_true", help="write the 50-item hand-label sheet")
    mode.add_argument("--agreement", action="store_true", help="write agreement.json from hand labels")
    parser.add_argument("--items", type=Path, default=ITEMS, help="items CSV (default: real items.csv)")
    parser.add_argument("--provider", choices=["laya", "fallback"], default="laya")
    parser.add_argument("--fallback-model", default=FALLBACK_MODEL,
                        help=f"Claude model for --provider fallback (default {FALLBACK_MODEL})")
    parser.add_argument("--workers", type=int, default=8, help="parallel API calls for the fallback")
    parser.add_argument("--batch-size", type=int, default=32, help="items per Laya forward pass")
    parser.add_argument("--sample", type=float, default=None,
                        help="score a fixed fraction of items (e.g. 0.5) to meet the runtime gate")
    args = parser.parse_args(argv)

    if args.agreement:
        write_agreement()
        return 0
    items = read_items(args.items)
    if args.handlabel:
        write_handlabel(items)
        return 0
    if not args.smoke and args.items.name.startswith("MOCK_"):
        sys.exit("Full runs score real items only; use --smoke with MOCK_ items.")
    provider = make_provider(args)
    if args.smoke:
        smoke(items, provider, args.batch_size)
        return 0
    if args.sample is not None:
        items = subsample(items, args.sample)
        print(f"Scoring a fixed {args.sample:.0%} subsample: {len(items)} items.")
    feats = score_items(items, provider, args.batch_size)
    feats.round(6).to_csv(FEATURES, index=False, lineterminator="\n")
    print(f"Wrote {rel(FEATURES)} ({len(feats)} rows, {provider.name}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
