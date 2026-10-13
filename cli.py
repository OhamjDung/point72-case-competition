from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from dks_model.engine import run_model
from dks_model.io import load_inputs
from dks_model.workbook import export_workbook


def _write_frame(frame: pd.DataFrame, output_format: str) -> None:
    if output_format == "json":
        print(frame.to_json(orient="records", indent=2, date_format="iso"))
    elif output_format == "csv":
        print(frame.to_csv(index=False), end="")
    else:
        for row in frame.to_dict(orient="records"):
            print(" | ".join(f"{key}={value}" for key, value in row.items()))


def _snapshot(outputs) -> dict:
    valuation = outputs.tables["valuation"]
    summary = outputs.tables["investment_summary"].iloc[0]
    return {
        "scenario": outputs.scenario,
        "model_mode": outputs.model_mode,
        "audit_status": outputs.audit_status,
        "reference_share_price": float(summary["reference_share_price"]),
        "scenario_weighted_value": float(summary["scenario_weighted_value"]),
        "rating": str(summary["rating"]),
        "valuation": {
            str(row["method"]): float(row["price_per_share"])
            for _, row in valuation.iterrows()
            if pd.notna(row["price_per_share"])
        },
        "diagnostics": outputs.diagnostics,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build, audit, and compare the DKS / Foot Locker model.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate schema, dates, sources, and economic bounds.")
    validate_parser.add_argument("--inputs", default="inputs", help="Input directory or JSON file.")

    audit_parser = subparsers.add_parser("audit", help="Run model audit checks.")
    audit_parser.add_argument("--inputs", default="inputs", help="Input directory or JSON file.")
    audit_parser.add_argument("--scenario", default=None, help="Scenario to audit.")
    audit_parser.add_argument("--format", choices=["text", "json", "csv"], default="text")
    audit_parser.add_argument("--strict", action="store_true", help="Return failure unless every audit is PASS.")

    build_parser = subparsers.add_parser("build", help="Build the formula-linked Excel workbook.")
    build_parser.add_argument("--inputs", default="inputs", help="Input directory or JSON file.")
    build_parser.add_argument("--output", default="outputs/DKS_model.xlsx", help="Workbook output path.")
    build_parser.add_argument("--scenario", default=None, help="Scenario to build.")
    build_parser.add_argument("--mode", choices=["sourced", "fixture"], required=True)

    backtest_parser = subparsers.add_parser("backtest", help="Report leakage-free rolling-origin diagnostics.")
    backtest_parser.add_argument("--inputs", default="inputs", help="Input directory or JSON file.")
    backtest_parser.add_argument("--format", choices=["text", "json", "csv"], default="text")

    compare_parser = subparsers.add_parser("compare", help="Attribute changes versus a preserved baseline snapshot.")
    compare_parser.add_argument("--inputs", default="inputs", help="Input directory or JSON file.")
    compare_parser.add_argument("--baseline", default="outputs/original_model_snapshot.json")
    compare_parser.add_argument("--format", choices=["text", "json", "csv"], default="text")
    compare_parser.add_argument("--write-snapshot", default=None, help="Optionally write the current machine-readable snapshot.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        inputs = load_inputs(args.inputs)
    except (ValidationError, ValueError) as exc:
        print(f"Input validation failed:\n{exc}")
        return 1

    if args.command == "validate":
        print(
            f"Input validation passed: schema={inputs.control.schema_version}, "
            f"mode={inputs.control.model_mode}, cutoff={inputs.control.data_cutoff}."
        )
        return 0

    if args.command == "build" and args.mode != inputs.control.model_mode:
        print(f"Build mode mismatch: requested {args.mode}, inputs are {inputs.control.model_mode}.")
        return 2

    scenario = getattr(args, "scenario", None) or inputs.control.selected_scenario
    outputs = run_model(inputs, scenario=scenario)

    if args.command == "audit":
        frame = pd.DataFrame([finding.model_dump() for finding in outputs.audit_findings])
        _write_frame(frame, args.format)
        if args.format == "text":
            print(f"Overall audit status: {outputs.audit_status}")
        return 2 if outputs.audit_status == "ERROR" or (args.strict and outputs.audit_status != "PASS") else 0

    if args.command == "build":
        output_path = Path(args.output)
        export_workbook(outputs, inputs, output_path)
        print(f"Workbook written to {output_path.resolve()}")
        print(f"Overall audit status: {outputs.audit_status}")
        return 2 if outputs.audit_status == "ERROR" else 0

    if args.command == "backtest":
        frame = outputs.tables["backtest_diagnostics"]
        _write_frame(frame, args.format)
        return 0 if str(frame.iloc[0].get("status")) == "PASS" else 3

    if args.command == "compare":
        current = _snapshot(outputs)
        if args.write_snapshot:
            snapshot_path = Path(args.write_snapshot)
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_text(json.dumps(current, indent=2), encoding="utf-8")
        baseline_path = Path(args.baseline)
        if not baseline_path.exists():
            print(f"Baseline snapshot not found: {baseline_path}")
            return 4
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        methods = sorted(set(baseline.get("valuation", {})) | set(current["valuation"]))
        rows = []
        for method in methods:
            before, after = baseline.get("valuation", {}).get(method), current["valuation"].get(method)
            rows.append({"metric": method, "original": before, "revised": after, "change": None if before is None or after is None else after - before})
        baseline_weighted = baseline.get("scenario_weighted_value")
        rows.append({"metric": "Scenario-weighted value", "original": baseline_weighted, "revised": current["scenario_weighted_value"], "change": None if baseline_weighted is None else current["scenario_weighted_value"] - baseline_weighted})
        _write_frame(pd.DataFrame(rows), args.format)
        return 0
    return 1
