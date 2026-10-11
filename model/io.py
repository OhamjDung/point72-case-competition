from __future__ import annotations

import json
from pathlib import Path

from dks_model.schemas import ModelInputs


def load_inputs(path: str | Path) -> ModelInputs:
    """Load a model input directory or JSON file."""
    path = Path(path)
    input_file = path / "model_inputs.json" if path.is_dir() else path
    with input_file.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return ModelInputs.model_validate(payload)
