from bankocr.recognition import recognize_digits, split_into_entries


def test_recognition_be_001_1_s1_two_entries_split_into_two_4_line_blocks():
    # GIVEN a scan file containing two entries, each consisting of 3 lines of
    # 27 characters and 1 blank line
    entry_1 = (
        "    _  _     _  _  _  _  _ \n"
        "  | _| _||_||_ |_   ||_||_|\n"
        "  ||_  _|  | _||_|  ||_| _|\n"
        "\n"
    )
    entry_2 = (
        "    _  _  _  _  _  _     _ \n"
        "|_||_|| ||_||_   |  |  ||_ \n"
        "  | _||_||_||_|  |  |  | _|\n"
        "\n"
    )
    scan_content = entry_1 + entry_2

    # WHEN Recognition reads the file and splits it into entries
    entries = split_into_entries(scan_content)

    # THEN two entries are identified
    assert len(entries) == 2
    # AND each entry has 3 lines of 27 characters
    assert len(entries[0]) == 3
    assert all(len(line) == 27 for line in entries[0])
    assert len(entries[1]) == 3
    assert all(len(line) == 27 for line in entries[1])


def test_recognition_be_001_2_s1_entry_with_digits_1_through_9_is_recognised():
    # GIVEN an entry whose 3 lines of 27 characters are:
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|",
    ]

    # WHEN Recognition converts the patterns to numeric digits
    account_number = recognize_digits(entry)

    # THEN the recognised account number is 123456789
    assert account_number == "123456789"


def test_recognition_be_001_2_s2_entry_containing_digit_0_is_recognised():
    # GIVEN an entry whose 3 lines of 27 characters are:
    entry = [
        "    _  _  _  _  _  _     _ ",
        "|_||_|| ||_||_   |  |  ||_ ",
        "  | _||_||_||_|  |  |  | _|",
    ]

    # WHEN Recognition converts the patterns to numeric digits
    account_number = recognize_digits(entry)

    # THEN the recognised account number is 490867715
    assert account_number == "490867715"
