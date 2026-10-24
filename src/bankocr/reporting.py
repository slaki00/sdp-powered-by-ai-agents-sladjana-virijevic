def format_result_line(account_number: str, status: str) -> str:
    """Format one result line from an account number and its validation status."""
    if status:
        return f"{account_number} {status}"
    return account_number


def write_result_file(lines: list[str], output_path: str) -> None:
    """Write formatted result lines to the result file, one line per entry."""
    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")


def _candidate_digits(pattern: str, digit_patterns: dict) -> list[str]:
    """Return all digits reachable by adding or removing exactly one segment.

    A segment is a single '|' or '_' in the 9-character pattern
    (3-char top + 3-char mid + 3-char bot).  Each alternative that matches
    a known pattern is included in the result.
    """
    candidates = []
    for i, ch in enumerate(pattern):
        for seg in ("|", "_"):
            if ch == seg:
                alt = pattern[:i] + " " + pattern[i + 1 :]
            elif ch == " ":
                alt = pattern[:i] + seg + pattern[i + 1 :]
            else:
                continue
            if alt in digit_patterns:
                candidates.append(digit_patterns[alt])
    return candidates


def correct_entry(
    entry: list[str],
    account_number: str,
    status: str,
    digit_patterns: dict,
    checksum_fn,
) -> tuple[str, str]:
    """Attempt to correct an ERR or ILL entry.

    For an ERR entry all nine positions are candidates for a single-segment
    change.  For an ILL entry only the '?' positions are candidates
    (REPORTING-BE-002.1-S1, REPORTING-BE-002.1-S2).
    Returns (corrected_number, "") when exactly one alternative passes the
    checksum, (account_number, "AMB") when more than one passes
    (REPORTING-BE-003.1), or (account_number, status) when none passes.
    """
    if status not in ("ERR", "ILL"):
        return account_number, status

    top, mid, bot = entry[0], entry[1], entry[2]

    candidate_positions = (
        range(9)
        if status == "ERR"
        else [i for i, d in enumerate(account_number) if d == "?"]
    )

    valid_alternatives = []
    for col in candidate_positions:
        start = col * 3
        pattern = (
            top[start : start + 3] + mid[start : start + 3] + bot[start : start + 3]
        )
        for alt_digit in _candidate_digits(pattern, digit_patterns):
            candidate = account_number[:col] + alt_digit + account_number[col + 1 :]
            if checksum_fn(candidate):
                valid_alternatives.append(candidate)

    if len(valid_alternatives) == 1:
        return valid_alternatives[0], ""
    # REPORTING-BE-003.1: more than one alternative passes → AMB
    if valid_alternatives:
        return account_number, "AMB"
    return account_number, status
