from bankocr.reporting import format_result_line, write_result_file


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
