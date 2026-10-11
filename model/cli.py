from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import ValidationError

from dks_model.engine import run_model
from dks_model.io import load_inputs
from dks_model.workbook import export_workbook


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and audit the DKS financial model.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate manual input templates.")
    validate_parser.add_argument("--inputs", default="inputs", help="Input directory or JSON file.")

    audit_parser = subparsers.add_parser("audit", help="Run model audit checks.")
    audit_parser.add_argument("--inputs", default="inputs", help="Input directory or JSON file.")
    audit_parser.add_argument("--scenario", default=None, help="Scenario to audit.")

    build_parser = subparsers.add_parser("build", help="Build Excel workbook.")
    build_parser.add_argument("--inputs", default="inputs", help="Input directory or JSON file.")
    build_parser.add_argument("--output", default="outputs/DKS_model.xlsx", help="Workbook output path.")
    build_parser.add_argument("--scenario", default=None, help="Scenario to build.")

    args = parser.parse_args(argv)
    try:
        inputs = load_inputs(args.inputs)
    except (ValidationError, ValueError) as exc:
        print(f"Input validation failed:\n{exc}")
        return 1

    scenario = getattr(args, "scenario", None) or inputs.control.selected_scenario

    if args.command == "validate":
        print("Input validation passed.")
        return 0

    outputs = run_model(inputs, scenario=scenario)
    if args.command == "audit":
        for finding in outputs.audit_findings:
            print(f"{finding.status}: {finding.check} - {finding.message}")
        print(f"Overall audit status: {outputs.audit_status}")
        return 0 if outputs.audit_status != "ERROR" else 2

    if args.command == "build":
        output_path = Path(args.output)
        export_workbook(outputs, inputs, output_path)
        print(f"Workbook written to {output_path}")
        print(f"Overall audit status: {outputs.audit_status}")
        return 0 if outputs.audit_status != "ERROR" else 2

    return 1
