from bankocr.recognition import DIGIT_PATTERNS
from bankocr.reporting import correct_entry, format_result_line, write_result_file
from bankocr.validation import checksum_passes


def test_reporting_be_001_1_s1_valid_number_has_no_marker():
    # GIVEN a recognised account number 345882865 with status valid
    account_number = "345882865"
    status = ""

    # WHEN the result line is formatted
    line = format_result_line(account_number, status)

    # THEN the line is "345882865"
    assert line == "345882865"


def test_reporting_be_001_1_s2_err_number_is_followed_by_err():
    # GIVEN a recognised account number 664371495 with status ERR
    account_number = "664371495"
    status = "ERR"

    # WHEN the result line is formatted
    line = format_result_line(account_number, status)

    # THEN the line is "664371495 ERR"
    assert line == "664371495 ERR"


def test_reporting_be_001_2_s1_two_entries_produce_two_line_result_file(tmp_path):
    # GIVEN two formatted lines: "345882865" and "664371495 ERR"
    lines = ["345882865", "664371495 ERR"]
    result_file = tmp_path / "result.txt"

    # WHEN the lines are written to the result file
    write_result_file(lines, str(result_file))

    # THEN the result file contains two lines
    written = result_file.read_text().splitlines()
    assert len(written) == 2
    # AND line 1 is "345882865"
    assert written[0] == "345882865"
    # AND line 2 is "664371495 ERR"
    assert written[1] == "664371495 ERR"


def test_reporting_be_002_1_s1_err_entry_replaced_by_single_valid_alternative():
    # GIVEN an entry whose three lines of 27 characters are:
    #  _  _     _  _        _  _
    # |_ |_ |_| _|  |  ||_||_||_
    # |_||_|  | _|  |  |  | _| _|
    entry = [
        " _  _     _  _        _  _ ",
        "|_ |_ |_| _|  |  ||_||_||_ ",
        "|_||_|  | _|  |  |  | _| _|",
    ]
    # AND Recognition produces "664371495" with status ERR
    # AND 664371495 fails the checksum: weighted sum 222, 222 mod 11 = 2
    account_number = "664371495"
    status = "ERR"

    # WHEN the correction is applied
    corrected_number, new_status = correct_entry(
        entry, account_number, status, DIGIT_PATTERNS, checksum_passes
    )

    # THEN the result for this entry is "664371485" with no marker
    assert corrected_number == "664371485"
    assert new_status == ""
    # AND 664371485 passes the checksum: weighted sum 220, 220 mod 11 = 0
    assert checksum_passes(corrected_number)


def test_reporting_be_002_1_s2_ill_entry_replaced_by_single_valid_alternative():
    # GIVEN an entry whose three lines of 27 characters are:
    #     _  _     _  _  _  _  _
    #   | _| _||_||_ |_   ||_||_|
    #    |_  _|  | _||_|  ||_| _|
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "   |_  _|  | _||_|  ||_| _|",
    ]
    # AND digit position 9 (leftmost) is a 1 pattern missing its bottom pipe;
    # Recognition produces "?23456789" with status ILL
    account_number = "?23456789"
    status = "ILL"

    # WHEN the correction is applied
    corrected_number, new_status = correct_entry(
        entry, account_number, status, DIGIT_PATTERNS, checksum_passes
    )

    # THEN the result for this entry is "123456789" with no marker
    assert corrected_number == "123456789"
    assert new_status == ""
    # AND 123456789 passes the checksum: weighted sum 165, 165 mod 11 = 0
    assert checksum_passes(corrected_number)


def test_reporting_be_002_2_s1_ill_entry_with_no_valid_alternative_keeps_ill():
    # GIVEN an entry whose three lines of 27 characters are
    # (the same entry as RECOGNITION-BE-002.1-S1):
    #     _  _  _  _  _  _  _  _
    #    | || || || || || || || |
    #    |_||_||_||_||_||_||_||_|
    entry = [
        "    _  _  _  _  _  _  _  _ ",
        "   | || || || || || || || |",
        "   |_||_||_||_||_||_||_||_|",
    ]
    # AND digit position 9 (leftmost) is an all-spaces pattern;
    # Recognition produces "?00000000" with status ILL
    account_number = "?00000000"
    status = "ILL"

    # WHEN the correction attempt completes
    corrected_number, new_status = correct_entry(
        entry, account_number, status, DIGIT_PATTERNS, checksum_passes
    )

    # THEN the result for this entry is "?00000000 ILL"
    assert corrected_number == "?00000000"
    assert new_status == "ILL"


def test_reporting_be_003_1_s1_err_entry_490067715_becomes_amb():
    # GIVEN an entry whose three lines of 27 characters are:
    #     _  _  _  _  _  _     _
    # |_||_|| || ||_   |  |  ||_
    #   | _||_||_||_|  |  |  | _|
    entry = [
        "    _  _  _  _  _  _     _ ",
        "|_||_|| || ||_   |  |  ||_ ",
        "  | _||_||_||_|  |  |  | _|",
    ]
    # AND Recognition produces "490067715" with status ERR
    # AND 490067715 fails the checksum: weighted sum 194, 194 mod 11 = 7
    # AND the correction search finds three alternatives that pass:
    #     490067115 (sum 176), 490067719 (sum 198), 490867715 (sum 242)
    account_number = "490067715"
    status = "ERR"

    # WHEN Reporting & Correction evaluates the alternatives
    corrected_number, new_status = correct_entry(
        entry, account_number, status, DIGIT_PATTERNS, checksum_passes
    )

    # THEN the status is changed from ERR to AMB
    assert new_status == "AMB"
    # AND the result for this entry is "490067715 AMB"
    assert corrected_number == "490067715"


def test_reporting_be_003_1_s2_err_entry_888888888_becomes_amb():
    # GIVEN an entry whose three lines of 27 characters are:
    #  _  _  _  _  _  _  _  _  _
    # |_||_||_||_||_||_||_||_||_|
    # |_||_||_||_||_||_||_||_||_|
    entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "|_||_||_||_||_||_||_||_||_|",
        "|_||_||_||_||_||_||_||_||_|",
    ]
    # AND Recognition produces "888888888" with status ERR
    # AND 888888888 fails the checksum: weighted sum 360, 360 mod 11 = 8
    # AND the correction search finds three alternatives that pass:
    #     888886888 (sum 352), 888888880 (sum 352), 888888988 (sum 363)
    account_number = "888888888"
    status = "ERR"

    # WHEN Reporting & Correction evaluates the alternatives
    corrected_number, new_status = correct_entry(
        entry, account_number, status, DIGIT_PATTERNS, checksum_passes
    )

    # THEN the status is changed from ERR to AMB
    assert new_status == "AMB"
    # AND the result for this entry is "888888888 AMB"
    assert corrected_number == "888888888"


def test_reporting_be_003_1_s3_err_entry_555555555_becomes_amb():
    # GIVEN an entry whose three lines of 27 characters are:
    #  _  _  _  _  _  _  _  _  _
    # |_ |_ |_ |_ |_ |_ |_ |_ |_
    #  _| _| _| _| _| _| _| _| _|
    entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "|_ |_ |_ |_ |_ |_ |_ |_ |_ ",
        " _| _| _| _| _| _| _| _| _|",
    ]
    # AND Recognition produces "555555555" with status ERR
    # AND 555555555 fails the checksum: weighted sum 225, 225 mod 11 = 5
    # AND the correction search finds two alternatives that pass:
    #     555655555 (sum 231), 559555555 (sum 253)
    account_number = "555555555"
    status = "ERR"

    # WHEN Reporting & Correction evaluates the alternatives
    corrected_number, new_status = correct_entry(
        entry, account_number, status, DIGIT_PATTERNS, checksum_passes
    )

    # THEN the status is changed from ERR to AMB
    assert new_status == "AMB"
    # AND the result for this entry is "555555555 AMB"
    assert corrected_number == "555555555"
