"""
CMVF Phase 2 Boundary Header — Project x Marquez
Prepends the boundary line to the audit log if it is not already the first line.
Does not validate. Does not produce output.
"""

import os

AUDIT_PATH = os.path.expanduser("~/ProjectX_Marquez/audit/chain.log")
BOUNDARY_PATH = os.path.expanduser("~/ProjectX_Marquez/validator/BOUNDARY.txt")

def main() -> None:
    if not os.path.exists(BOUNDARY_PATH):
        print("BOUNDARY: file not found")
        return

    with open(BOUNDARY_PATH, "r") as f:
        boundary = f.read().strip()

    if not os.path.exists(AUDIT_PATH):
        with open(AUDIT_PATH, "w") as f:
            f.write(boundary + "\n")
        print("HEADER: written")
        return

    with open(AUDIT_PATH, "r") as f:
        first = f.readline().strip()

    if first == boundary:
        print("HEADER: already present")
        return

    with open(AUDIT_PATH, "r") as f:
        rest = f.read()

    with open(AUDIT_PATH, "w") as f:
        f.write(boundary + "\n" + rest)

    print("HEADER: prepended")

if __name__ == "__main__":
    main()
