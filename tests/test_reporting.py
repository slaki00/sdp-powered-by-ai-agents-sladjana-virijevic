from bankocr.reporting import format_result_line


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
