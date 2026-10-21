from cmvf_validator import CMVFValidator

def main() -> None:
    validator = CMVFValidator(scac="TEST", run_date="2026-10-20")

    result = validator.run(raw_rows=[])
    print("Empty:", "PASS" if result else "REFUSE")

    row = {"scac": "TEST", "date": "2026-10-20", "on_time": 95, "total_shipments": 100}
    result = validator.run(raw_rows=[row])
    print("Valid:", "PASS" if result else "REFUSE")
    if result:
        print("OTR:", result["metrics"]["on_time_rate"])

if __name__ == "__main__":
    main()
