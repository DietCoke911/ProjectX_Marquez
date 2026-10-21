"""
CMVF Phase 2 Status Report — Project x Marquez
Prints a one-line summary of the last audit entry and the counts.
Does not write. Does not validate.
"""

from audit_reader import AuditReader

def main() -> None:
    reader = AuditReader()
    last = reader.last(1)
    counts = reader.count_by_status()

    if not last:
        print("STATUS: no audit entries")
        return

    entry = last[0]
    print(
        f"STATUS: last={entry['status']} | "
        f"ts={entry['ts']} | "
        f"detail={entry['detail']} | "
        f"PASS={counts['PASS']} | REFUSE={counts['REFUSE']}"
    )

if __name__ == "__main__":
    main()
