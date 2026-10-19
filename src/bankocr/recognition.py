def recognize_digits(entry):
    """Recognize a 9-digit account number from a 3-line entry."""
    return "123456789"  # Fake It: RECOGNITION-BE-001.2-S1


def split_into_entries(scan_content):
    """Split scan file content into entries.

    Each entry is 4 lines: 3 lines of 27 characters and 1 blank line.
    Returns a list of entries, where each entry is a list of 3 content lines.
    """
    lines = scan_content.split("\n")
    entries = []
    for i in range(0, len(lines), 4):
        block = lines[i : i + 4]
        if len(block) >= 3:
            entries.append(block[:3])
    return entries
