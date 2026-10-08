# Point72 Academy 2026 Case Competition: Research Plan

**Deadline:** Oct 12, 2026, 11:59 PM ET (pitch + model). Today is Oct 6, so about 6 days remain.
**Universe:** PHVS (Pharvaris), NBIS (Nebius Group), DKS (Dick's Sporting Goods), FTAI (FTAI Aviation)
**Goal of the research phase:** choose the ticker where a public-data investigation can *settle a contested question about the company's economics*, then build the evidence base for 1–2 variant insights.

## Selection rubric (scored 1–5 per ticker)
1. **Settleable debate.** Is there a contested question about the economics that public data can actually answer?
2. **Original-data potential.** Are there free external datasets that let us build something consensus doesn't have?
3. **Modelability.** Can revenue and costs be tied to operating drivers? This matters because we need 2+ years of history, 5 years of projections and 2 years quarterly.
4. **12-month catalyst.** Is there a dated event that would make the market recognize the view?
5. **Crowdedness (inverse).** How far from the consensus or GenAI narrative can we credibly get?

Tie-break: prefer the ticker where public operating data settles a dispute over the one with the most exciting story.

## Phase 1: Screen (Day 1, Oct 6–7)
- 4 parallel Sonnet agents, one per ticker. Each writes `research/<TICKER>/screen.md` and returns a scorecard of 250 words or less.
- Orchestrator (Opus) challenges weak claims, ranks the tickers and recommends one. **The user picks.**

## Phase 1.5: Stress tests (Oct 6, at the user's request)
Each ticker gets the same three tests, written to `research/<TICKER>/stress_test.md`:
- **Smoke tests:** a PASS/FAIL check of each thesis's load-bearing facts against primary sources.
- **Ablation:** a simple valuation, then remove each thesis pillar one at a time and record how the value per share changes. The point is to identify which pillar actually carries the insight.
- **Counter-case:** the strongest opposing case, quantified.

Each ticker ends in a verdict:
- viable or not
- direction
- price target and % gap to the current price
- P(right)
- expected alpha = P×gap − (1−P)×adverse move
- kill criteria

The ticker is chosen on expected alpha, evidence strength and team fit.

## Phase 2: Deep dive on the chosen ticker (Days 2–4, Oct 7–9)
3–5 Sonnet agents, split by question rather than by deck section:
- **A. Core debate.** Test variant hypothesis #1 against primary sources (filings, transcripts, regulatory data).
- **B. Original dataset.** Build the external-data evidence (registry scrape, trial data, store/traffic data, etc.) and save it as CSV.
- **C. Consensus and model inputs.** Pull historical financials (EDGAR XBRL), free consensus, share count, debt and comps.
- **D. Bear case.** Gather the strongest disconfirming evidence, short reports and management rebuttals.
- **E. (optional) Variant hypothesis #2.**

The orchestrator verifies key numbers against primary sources and writes `research/<TICKER>/thesis.md`.

## Phase 3: Model (Days 4–5, Oct 9–10)
Build an Excel model from a blank workbook. It needs:
- a Summary tab
- 2+ years of history
- 5 years of projections, with 2 years quarterly
- flagged key drivers
- sensitivities
- a bridge from consensus to our case

## Phase 4: Deck + GenAI appendix (Days 5–6, Oct 10–12)
- 12 slides max, with the appendix counted inside that 12.
- Cite sources on every slide.
- Page numbers and team name on all documents.

## Compliance (applies to every agent)
- Public sources only.
- Never contact companies or individuals.
- No paywalled or leaked content.
- Don't reproduce any other firm's or person's model.
- Log all GenAI prompts and responses in `genai_log/` for the appendix.
