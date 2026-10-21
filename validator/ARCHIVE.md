# CMVF Phase 2 Archive Note — Project x Marquez

## Active Chain

These files form the current path from raw rows to carrier-facing text or refuse:

- entry_point.py
- run_coordinator.py
- contract_consumer.py
- output_formatter.py
- contract_executor.py
- end_to_end.py
- audit_writer.py
- audit_reader.py
- status_report.py
- confirm_chain.py
- refuse_test.py
- cr_rules.py

## Retained for Reference

These files remain in the directory. They are not called by the active chain:

- cmvf_validator.py
- contract_verifier.py
- contract_writer.py
- gate_runner.py
- test_harness.py

## Boundary

Carrier-facing text is produced only from a verified contract.
Every refuse is logged.
No module produces output by self-validation.

