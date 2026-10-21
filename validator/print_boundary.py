"""
CMVF Phase 2 Boundary Printer — Project x Marquez
Prints the current boundary in one line.
Does not write. Does not validate.
"""

import os

BOUNDARY_PATH = os.path.expanduser("~/ProjectX_Marquez/validator/BOUNDARY.txt")

def main() -> None:
    if not os.path.exists(BOUNDARY_PATH):
        print("BOUNDARY: file not found")
        return
    with open(BOUNDARY_PATH, "r") as f:
        line = f.read().strip()
    print(line)

if __name__ == "__main__":
    main()
