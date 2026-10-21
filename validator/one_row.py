from cmvf_validator import CMVFValidator

def main() -> None:
    validator = CMVFValidator(scac="TEST", run_date="2026-10-18")
    row = {
        "scac": "TEST",
        "date": "2026-10-18",
        "on_time": 98,
        "total_shipments": 100,
    }
    result = validator.run(raw_rows=[row])
    print("Result:", "PASS" if result else "REFUSE")
    if result:
        print("OTR:", result["metrics"]["on_time_rate"])

if __name__ == "__main__":
    main()
