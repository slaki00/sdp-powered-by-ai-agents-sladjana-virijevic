# Each digit is represented as a 9-character string: the 3-character top row,
# followed by the 3-character middle row, followed by the 3-character bottom row.
DIGIT_PATTERNS = {
    " _ " "| |" "|_|": "0",
    "   " "  |" "  |": "1",
    " _ " " _|" "|_ ": "2",
    " _ " " _|" " _|": "3",
    "   " "|_|" "  |": "4",
    " _ " "|_ " " _|": "5",
    " _ " "|_ " "|_|": "6",
    " _ " "  |" "  |": "7",
    " _ " "|_|" "|_|": "8",
    " _ " "|_|" " _|": "9",
}


def recognize_digits(entry):
    """Recognise a 9-digit account number from a 3-line entry.

    Each entry is a list of 3 lines of 27 characters. Each group of 3
    columns represents one digit matched against the known patterns.
    An unrecognised pattern produces '?' in that position
    (RECOGNITION-BE-002.1).
    """
    top, mid, bot = entry[0], entry[1], entry[2]
    account_number = ""
    for col in range(9):
        start = col * 3
        pattern = (
            top[start : start + 3] + mid[start : start + 3] + bot[start : start + 3]
        )
        account_number += DIGIT_PATTERNS.get(pattern, "?")  # RECOGNITION-BE-002.1
    return account_number


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
