from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from dks_model.schemas import ModelInputs, ModelOutputs


SHEET_ORDER = [
    "Investment Summary",
    "Model Control Panel",
    "Historical Financials",
    "Historical Segment Recon",
    "Assumptions & Sources",
    "Legacy DICK'S Operating Model",
    "Foot Locker Operating Model",
    "Foot Locker Store Cohorts",
    "Acquisition & Synergy",
    "Consolidated Income Statement",
    "Working Capital Schedule",
    "Capex & Depreciation",
    "Debt Interest Lease",
    "Share Count Capital Alloc",
    "Consolidated Balance Sheet",
    "Consolidated Cash Flow",
    "Financial Ratios & ROIC",
    "Wall Street Consensus",
    "Consensus Variant Bridge",
    "Valuation Bridge",
    "Discounted Cash Flow",
    "SOTP Valuation",
    "Relative Valuation",
    "Reverse DCF",
    "Scenarios & Sensitivities",
    "Probabilistic Valuation",
    "Alternative Data & Backtesting",
    "Thesis Catalysts Monitoring",
    "Forecast Variance Analysis",
    "Model Audit & Quality Checks",
]


def _clean_value(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if np.isnan(value) or np.isinf(value) else float(value)
    if isinstance(value, float):
        return None if not np.isfinite(value) else value
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if pd.isna(value):
        return None
    return value


def _records(frame: pd.DataFrame) -> list[dict]:
    materialized = frame.reset_index() if frame.index.name else frame.copy()
    return [{str(key): _clean_value(value) for key, value in row.items()} for row in materialized.to_dict(orient="records")]


def build_workbook_payload(outputs: ModelOutputs, inputs: ModelInputs) -> dict:
    return {
        "inputs": inputs.model_dump(mode="json"),
        "outputs": {
            "scenario": outputs.scenario,
            "model_mode": outputs.model_mode,
            "audit_status": outputs.audit_status,
            "diagnostics": outputs.diagnostics,
            "tables": {name: _records(frame) for name, frame in outputs.tables.items()},
            "audit_findings": [item.model_dump(mode="json") for item in outputs.audit_findings],
        },
        "sheet_order": SHEET_ORDER,
    }


def _runtime_paths() -> tuple[Path, Path]:
    node = os.environ.get("DKS_NODE_BIN")
    modules = os.environ.get("DKS_ARTIFACT_NODE_MODULES")
    if node and modules:
        return Path(node), Path(modules)
    runtime = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node"
    candidate_node = runtime / "bin" / ("node.exe" if os.name == "nt" else "node")
    candidate_modules = runtime / "node_modules"
    if candidate_node.exists() and candidate_modules.exists():
        return candidate_node, candidate_modules
    path_node = shutil.which("node")
    local_modules = Path("node_modules").resolve()
    if path_node and local_modules.exists():
        return Path(path_node), local_modules
    raise RuntimeError(
        "Artifact workbook runtime not found. Set DKS_NODE_BIN and "
        "DKS_ARTIFACT_NODE_MODULES, or run inside the documented Codex workspace runtime."
    )


def _ensure_node_modules_junction(build_dir: Path, modules: Path) -> None:
    junction = build_dir / "node_modules"
    if junction.exists():
        return
    if os.name == "nt":
        command = (
            f"New-Item -ItemType Junction -Path '{junction}' -Target '{modules}' "
            "| Out-Null"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", command], check=True)
    else:
        junction.symlink_to(modules, target_is_directory=True)


def export_workbook(outputs: ModelOutputs, inputs: ModelInputs, path: str | Path) -> None:
    """Build the formula-linked XLSX through the artifact-tool JavaScript layer."""
    output_path = Path(path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    project_root = Path(__file__).resolve().parents[2]
    source_builder = project_root / "scripts" / "build_workbook.mjs"
    if not source_builder.exists():
        raise RuntimeError(f"Workbook builder is missing: {source_builder}")
    build_dir = project_root / ".tmp" / "artifact-workbook-build"
    build_dir.mkdir(parents=True, exist_ok=True)
    payload_path = build_dir / "workbook_payload.json"
    runtime_builder = build_dir / "build_workbook.mjs"
    payload_path.write_text(json.dumps(build_workbook_payload(outputs, inputs), indent=2, allow_nan=False), encoding="utf-8")
    shutil.copyfile(source_builder, runtime_builder)
    node, modules = _runtime_paths()
    _ensure_node_modules_junction(build_dir, modules)
    subprocess.run([str(node), str(runtime_builder), str(payload_path), str(output_path)], check=True, cwd=build_dir)
