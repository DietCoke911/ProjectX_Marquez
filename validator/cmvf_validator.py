from datetime import datetime, timezone
from typing import Any, Dict, List
import json
import os
import sys

CONTRACT_VERSION = "1.0"

class CMVFValidator:
    def __init__(self, scac: str, run_date: str):
        self.scac = scac
        self.run_date = run_date
        self.halted = False
        self.audit_log: List[Dict[str, Any]] = []

    def _log(self, stage: str, status: str, detail: str) -> None:
        ts = datetime.now(timezone.utc).isoformat()
        entry = {
            "timestamp": ts,
            "stage": stage,
            "status": status,
            "detail": detail,
            "scac": self.scac,
            "run_date": self.run_date,
        }
        self.audit_log.append(entry)

        line = f"{ts} | {status} | {stage}: {detail}"
        audit_path = os.path.expanduser("~/ProjectX_Marquez/audit/chain.log")
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        with open(audit_path, "a") as f:
            f.write(line + "\n")

        jsonl_path = os.path.expanduser("~/ProjectX_Marquez/audit/chain.jsonl")
        with open(jsonl_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def filter_lock(self, raw_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not raw_rows:
            self._log("Filter Lock", "REFUSE", "Empty input — no rows provided")
            self.halted = True
            return []
        clean = []
        for row in raw_rows:
            if not isinstance(row, dict):
                self._log("Filter Lock", "REFUSE", f"Non-dict row rejected: {type(row)}")
                continue
            required = {"scac", "date", "on_time", "total_shipments"}
            missing = required - set(row.keys())
            if missing:
                self._log("Filter Lock", "REFUSE", f"Row missing fields: {missing}")
                continue
            clean.append(row)
        if not clean:
            self._log("Filter Lock", "REFUSE", "All rows rejected by Filter Lock")
            self.halted = True
        else:
            self._log("Filter Lock", "PASS", f"{len(clean)} rows passed")
        return clean

    def calculation_engine(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not rows:
            self._log("Calculation Engine", "REFUSE", "No rows to calculate")
            self.halted = True
            return {}
        total = sum(r.get("total_shipments", 0) for r in rows)
        on_time = sum(r.get("on_time", 0) for r in rows)
        rate = (on_time / total * 100) if total else 0.0
        metrics = {
            "total_shipments": total,
            "on_time_shipments": on_time,
            "on_time_rate": round(rate, 2),
        }
        self._log("Calculation Engine", "PASS", f"OTR={metrics['on_time_rate']}")
        return metrics

    def validation_gates(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        if not metrics:
            self._log("Validation Gates", "REFUSE", "No metrics to validate")
            self.halted = True
            return {}
        rate = metrics.get("on_time_rate", 0)
        gate = "PASS" if rate >= 95.0 else "REFUSE"
        detail = f"OTR {rate} {'meets' if gate == 'PASS' else 'below'} 95% threshold"
        self._log("Validation Gates", gate, detail)
        if gate == "REFUSE":
            self.halted = True
        return {"on_time_rate_gate": gate, "threshold": 95.0, "actual": rate}

    def confidence_scorer(self, gate_results: Dict[str, Any]) -> Dict[str, Any]:
        if not gate_results:
            self._log("Confidence Scorer", "REFUSE", "No gate results")
            self.halted = True
            return {}
        gate_keys = [k for k in gate_results if k.endswith("_gate")]
        passed = sum(1 for k in gate_keys if gate_results[k] == "PASS")
        total = len(gate_keys)
        score = round((passed / total) * 100, 1) if total else 0.0
        self._log("Confidence Scorer", "PASS", f"Confidence={score}")
        return {"confidence_score": score, "gates_passed": passed, "gates_total": total}

    def output_packager(self, metrics: Dict[str, Any], gate_results: Dict[str, Any], confidence: Dict[str, Any]) -> Dict[str, Any]:
        contract = {
            "contract_id": f"CMVF-{self.scac}-{self.run_date}",
            "contract_version": CONTRACT_VERSION,
            "scac": self.scac,
            "run_date": self.run_date,
            "metrics": metrics,
            "gate_results": gate_results,
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "producer": "CMVFValidator",
            "consumer_note": "Executor must not send data back to validator.",
        }
        self._log("Output Packager", "PASS", f"Contract {contract['contract_id']} written")
        return contract

    def reject_return(self, data: Any) -> None:
        self._log("Return Boundary", "REFUSE", f"Return data rejected: {type(data).__name__}")
        raise ValueError("Validator does not accept return data from executor.")

    def run(self, raw_rows: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        self.halted = False
        rows = self.filter_lock(raw_rows)
        if self.halted:
            return None
        metrics = self.calculation_engine(rows)
        if self.halted:
            return None
        gates = self.validation_gates(metrics)
        if self.halted:
            return None
        confidence = self.confidence_scorer(gates)
        if self.halted:
            return None
        contract = self.output_packager(metrics, gates, confidence)

        # Persist contract
        out_dir = os.path.expanduser("~/ProjectX_Marquez/contracts")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{contract['contract_id']}.json")
        with open(out_path, "w") as f:
            json.dump(contract, f, indent=2)
        self._log("Output Packager", "PASS", f"Contract written to {out_path}")
        return contract

    def get_audit_log(self) -> List[Dict[str, Any]]:
        return self.audit_log


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cmvf_validator.py <input.json>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        data = json.load(f)
    scac = data.get("scac", "UNKNOWN")
    run_date = data.get("run_date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    rows = data.get("rows", [])
    v = CMVFValidator(scac, run_date)
    contract = v.run(rows)
    if contract is None:
        print("REFUSED — no contract written")
        sys.exit(1)
    print(f"CONTRACT WRITTEN: ~/ProjectX_Marquez/contracts/{contract['contract_id']}.json")


if __name__ == "__main__":
    main()
