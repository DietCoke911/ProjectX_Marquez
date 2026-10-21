# CMVF Phase 2 — Project x Marquez

## Boundary

The chain produces carrier-facing text only from a verified contract.
Every refuse is logged.
No module produces output by self-validation.

## Current Path

raw rows → entry_point → run_coordinator → contract → contract_executor → contract_consumer → output_formatter → carrier-facing text

Any gate that returns None stops the chain and writes a REFUSE line.

## Confirmed

- Known-good rows produce output and a PASS line.
- Known-bad rows produce no output and a REFUSE line.
- Status report reads the last line and the counts.

## Modules

See `python3 file_summary.py` for the current list.

