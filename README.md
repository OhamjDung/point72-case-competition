# DKS Financial Model

This project builds a greenfield Python financial model for DICK'S Sporting
Goods and the acquired Foot Locker operations. It produces both a reusable
calculation engine and an Excel workbook with professional model tabs,
scenario outputs, valuation schedules, source tracking, and audit checks.

The bundled input file is an illustrative template. Replace it with
source-verified values from SEC filings, company releases, consensus services,
and internal research before relying on any investment conclusion.

## Commands

```powershell
python -m dks_model validate --inputs inputs
python -m dks_model audit --inputs inputs
python -m dks_model build --inputs inputs --output outputs/DKS_model.xlsx
```

## Design

- `src/dks_model/schemas.py` defines typed input and output contracts.
- `src/dks_model/io.py` loads and validates manual JSON input templates.
- `src/dks_model/engine.py` runs the deterministic operating model,
  integrated statements, valuation, reverse DCF, scenarios, sensitivities,
  probabilistic valuation, catalyst monitoring, and forecast variance tracking.
- `src/dks_model/workbook.py` exports the model to Excel using `xlsxwriter`.
- `tests/` validates the engine, audit behavior, CLI, and workbook output.

## Input Philosophy

The first release intentionally uses manual structured inputs. This keeps the
core model auditable and avoids quietly inventing unavailable consensus,
alternative data, or analyst estimates. Automated SEC and market-data ingestion
can be added later behind the same `ModelInputs` contract.

## Phase 2 Risk Workflow

The current model includes manual-input Phase 2 additions for Monte Carlo-style
probabilistic valuation, thesis catalyst monitoring, and forecast variance
tracking. The `Alternative Data & Backtesting` workbook tab is intentionally
reserved for future collection and validation methods.
