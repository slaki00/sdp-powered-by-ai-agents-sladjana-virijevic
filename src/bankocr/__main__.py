"""CLI Entry Point for BankOCR.

Usage:
    python -m bankocr [scan_file result_file]

Defaults (ADR-004):
    scan_file   /data/scan.txt
    result_file /data/result.txt
"""

import sys

from bankocr.recognition import DIGIT_PATTERNS, recognize_digits, split_into_entries
from bankocr.reporting import correct_entry, format_result_line, write_result_file
from bankocr.validation import assign_status, checksum_passes


def main(scan_path: str, result_path: str) -> None:
    """Read scan_path, recognise and validate each entry, write result_path."""
    try:
        with open(scan_path, encoding="utf-8") as f:
            scan_content = f.read()
    except OSError as exc:
        # RECOGNITION-BE-003.1: plain message to stderr, no traceback
        print(
            f"Error: cannot read scan file '{scan_path}': {exc.strerror}",
            file=sys.stderr,
        )
        sys.exit(1)

    entries = split_into_entries(scan_content)
    lines = []
    for entry in entries:
        account_number = recognize_digits(entry)
        status = assign_status(account_number)
        # REPORTING-BE-002.1: attempt correction for ERR and ILL entries
        account_number, status = correct_entry(
            entry, account_number, status, DIGIT_PATTERNS, checksum_passes
        )
        lines.append(format_result_line(account_number, status))

    write_result_file(lines, result_path)


if __name__ == "__main__":
    args = sys.argv[1:]
    scan = args[0] if len(args) > 0 else "/data/scan.txt"
    result = args[1] if len(args) > 1 else "/data/result.txt"
    main(scan, result)
