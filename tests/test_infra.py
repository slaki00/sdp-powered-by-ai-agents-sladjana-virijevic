import subprocess
import sys


def test_recognition_infra_001_1_s1_recognition_runs_inside_the_container(
    tmp_path,
):
    # GIVEN a data folder contains a scan.txt with one entry representing 123456789
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _     _  _  _  _  _ \n"
        "  | _| _||_||_ |_   ||_||_|\n"
        "  ||_  _|  | _||_|  ||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the container reads /data/scan.txt and writes /data/result.txt
    assert result_file.exists()
    # AND data/result.txt contains "123456789" with no marker
    assert result_file.read_text(encoding="utf-8").splitlines() == ["123456789"]
    # AND the container exits with code 0
    assert result.returncode == 0


def test_recognition_infra_001_2_s1_scan_file_is_read_from_the_mounted_data_folder(
    tmp_path,
):
    # GIVEN a data folder contains scan.txt with one entry representing 345882865
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n",
        encoding="utf-8",
    )
    # AND no result.txt exists in the data folder
    assert not result_file.exists()

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN data/result.txt is created on the local machine
    assert result_file.exists()
    # AND data/result.txt contains "345882865" with no marker
    assert result_file.read_text(encoding="utf-8").splitlines() == ["345882865"]


def test_recognition_infra_001_3_s1_recognised_entries_produce_no_diagnostic_messages(
    tmp_path,
):
    # GIVEN a scan file containing one entry representing 123456789
    # where all digits are recognised
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _     _  _  _  _  _ \n"
        "  | _| _||_||_ |_   ||_||_|\n"
        "  ||_  _|  | _||_|  ||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN nothing is written to standard error
    assert result.stderr == ""
    # AND data/result.txt is the only file written to the data folder
    written = [p.name for p in tmp_path.iterdir() if p != scan_file]
    assert written == ["result.txt"]


def test_recognition_story_001_s1_multiple_entries_recognised_in_one_scan_file(
    tmp_path,
):
    # GIVEN a scan file with two entries representing 123456789 and 345882865
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _     _  _  _  _  _ \n"
        "  | _| _||_||_ |_   ||_||_|\n"
        "  ||_  _|  | _||_|  ||_| _|\n"
        "\n"
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result file has two lines
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    # AND line 1 is "123456789" with no marker
    assert lines[0] == "123456789"
    # AND line 2 is "345882865" with no marker
    assert lines[1] == "345882865"


def test_validation_infra_001_1_s1_validation_runs_inside_the_container(tmp_path):
    # GIVEN the BankOCR image has been built with `docker build -t bankocr .`
    # AND a data folder contains a scan.txt with one entry representing 345882865
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the container reads /data/scan.txt and writes /data/result.txt
    assert result_file.exists()
    # AND data/result.txt contains "345882865" with no marker
    assert result_file.read_text(encoding="utf-8").splitlines() == ["345882865"]
    # AND the container exits with code 0
    assert result.returncode == 0


def test_validation_infra_001_2_s1_result_with_err_stored_in_data_folder(tmp_path):
    # GIVEN a data folder contains scan.txt with one entry representing 222222222
    # AND no result.txt exists in the data folder
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _  _  _  _  _  _  _  _  _ \n"
        " _| _| _| _| _| _| _| _| _|\n"
        "|_ |_ |_ |_ |_ |_ |_ |_ |_ \n"
        "\n",
        encoding="utf-8",
    )
    assert not result_file.exists()

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN data/result.txt is created on the local machine
    assert result_file.exists()
    # AND data/result.txt contains "222222222 ERR"
    assert result_file.read_text(encoding="utf-8").splitlines() == ["222222222 ERR"]


def test_validation_infra_001_3_s1_err_entries_produce_no_diagnostic_messages(
    tmp_path,
):
    # GIVEN a scan file containing 345882865 and 222222222
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _  _  _  _  _  _  _  _ \n"
        " _| _| _| _| _| _| _| _| _|\n"
        "|_ |_ |_ |_ |_ |_ |_ |_ |_ \n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN nothing is written to standard error
    assert result.stderr == ""
    # AND data/result.txt is the only file written to the data folder
    written = [p.name for p in tmp_path.iterdir() if p != scan_file]
    assert written == ["result.txt"]


def test_validation_story_001_s1_valid_and_invalid_numbers_in_one_file(tmp_path):
    # GIVEN a scan file with two entries: 345882865 and 222222222
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _  _  _  _  _  _  _  _ \n"
        " _| _| _| _| _| _| _| _| _|\n"
        "|_ |_ |_ |_ |_ |_ |_ |_ |_ \n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result file has two lines
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    # AND line 1 is "345882865" with no marker
    assert lines[0] == "345882865"
    # AND line 2 is "222222222 ERR"
    assert lines[1] == "222222222 ERR"


def test_reporting_infra_001_1_s1_reporting_runs_inside_the_container(tmp_path):
    # GIVEN a data folder contains a scan.txt with two entries
    # representing 345882865 and 222222222
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _  _  _  _  _  _  _  _ \n"
        " _| _| _| _| _| _| _| _| _|\n"
        "|_ |_ |_ |_ |_ |_ |_ |_ |_ \n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the container reads /data/scan.txt and writes /data/result.txt
    assert result_file.exists()
    # AND data/result.txt contains "345882865" on line 1 and "222222222 ERR" on line 2
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "345882865"
    assert lines[1] == "222222222 ERR"
    # AND the container exits with code 0
    assert result.returncode == 0


def test_reporting_infra_001_2_s1_result_file_written_to_mounted_data_folder(
    tmp_path,
):
    # GIVEN a data folder contains scan.txt with two entries
    # representing 345882865 and 222222222
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _  _  _  _  _  _  _  _ \n"
        " _| _| _| _| _| _| _| _| _|\n"
        "|_ |_ |_ |_ |_ |_ |_ |_ |_ \n"
        "\n",
        encoding="utf-8",
    )
    # AND no result.txt exists in the data folder
    assert not result_file.exists()

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN data/result.txt is created on the local machine
    assert result_file.exists()
    # AND data/result.txt contains "345882865" on line 1 and "222222222 ERR" on line 2
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "345882865"
    assert lines[1] == "222222222 ERR"


def test_reporting_infra_001_3_s1_err_entries_produce_no_diagnostic_messages(
    tmp_path,
):
    # GIVEN a scan file containing 345882865 and 222222222
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _  _  _  _  _  _  _  _ \n"
        " _| _| _| _| _| _| _| _| _|\n"
        "|_ |_ |_ |_ |_ |_ |_ |_ |_ \n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN nothing is written to standard error
    assert result.stderr == ""
    # AND data/result.txt is the only file written to the data folder
    written = [p.name for p in tmp_path.iterdir() if p != scan_file]
    assert written == ["result.txt"]


def test_reporting_story_001_s1_valid_and_err_entries_written_in_order(tmp_path):
    # GIVEN a scan file with three entries: 345882865, 222222222 and 123456789
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _  _  _  _  _  _  _  _ \n"
        " _| _| _| _| _| _| _| _| _|\n"
        "|_ |_ |_ |_ |_ |_ |_ |_ |_ \n"
        "\n"
        "    _  _     _  _  _  _  _ \n"
        "  | _| _||_||_ |_   ||_||_|\n"
        "  ||_  _|  | _||_|  ||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result file has three lines
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    # AND line 1 is "345882865" with no marker
    assert lines[0] == "345882865"
    # AND line 2 is "222222222 ERR"
    assert lines[1] == "222222222 ERR"
    # AND line 3 is "123456789" with no marker
    assert lines[2] == "123456789"


def test_validation_infra_002_1_s1_bankocr_marks_ill_entry_inside_container(
    tmp_path,
):
    # GIVEN the BankOCR image has been built with `docker build -t bankocr .`
    # AND a data folder contains scan.txt with two entries:
    #   - first: all-spaces grid at digit position 1, eight 0 patterns at 2-9
    #   - second: account number 345882865
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _  _  _  _  _  _  _ \n"
        "   | || || || || || || || |\n"
        "   |_||_||_||_||_||_||_||_|\n"
        "\n"
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN data/result.txt on the local machine contains two lines
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    # AND the first line is "?00000000 ILL"
    assert lines[0] == "?00000000 ILL"
    # AND the second line is "345882865"
    assert lines[1] == "345882865"
    # AND the container exits with code 0
    assert result.returncode == 0


def test_validation_story_002_s1_unreadable_digit_marked_ill_valid_no_marker(
    tmp_path,
):
    # GIVEN a scan file with two entries:
    # - first: all-spaces grid at digit position 1 and eight 0 patterns at 2-9;
    #   its three lines of 27 characters are:
    #       _  _  _  _  _  _  _  _
    #      | || || || || || || || |
    #      |_||_||_||_||_||_||_||_|
    # - second: account number 345882865
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _  _  _  _  _  _  _ \n"
        "   | || || || || || || || |\n"
        "   |_||_||_||_||_||_||_||_|\n"
        "\n"
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result file has two lines
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    # AND line 1 is "?00000000 ILL"
    assert lines[0] == "?00000000 ILL"
    # AND line 2 is "345882865" with no marker
    assert lines[1] == "345882865"


def test_recognition_infra_002_1_s1_bankocr_processes_scan_with_unreadable_digit(
    tmp_path,
):
    # GIVEN the BankOCR image has been built with `docker build -t bankocr .`
    # AND a data folder contains scan.txt with two entries:
    #   - first: all-spaces grid at digit position 1, eight 0 patterns at 2-9
    #   - second: account number 123456789
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _  _  _  _  _  _  _ \n"
        "   | || || || || || || || |\n"
        "   |_||_||_||_||_||_||_||_|\n"
        "\n"
        "    _  _     _  _  _  _  _ \n"
        "  | _| _||_||_ |_   ||_||_|\n"
        "  ||_  _|  | _||_|  ||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the CLI is run as python -m bankocr <scan_file> <result_file>
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN data/result.txt on the local machine contains two lines
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    # AND the first line is "?00000000 ILL"
    assert lines[0] == "?00000000 ILL"
    # AND the second line is "123456789"
    assert lines[1] == "123456789"
    # AND the container exits with code 0
    assert result.returncode == 0


def test_validation_story_002_s2_all_nine_unreadable_marked_ill(tmp_path):
    # GIVEN a scan file with one entry where all nine 3-by-3 grids are
    # the all-spaces pattern; its three lines of 27 characters are:
    #    (27 spaces)
    #    (27 spaces)
    #    (27 spaces)
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "                           \n"
        "                           \n"
        "                           \n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result file has one line
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    # AND line 1 is "????????? ILL"
    assert lines[0] == "????????? ILL"


def test_recognition_story_002_s1_unreadable_digit_marked_and_processing_continues(
    tmp_path,
):
    # GIVEN a scan file with two entries:
    # - first: all-spaces grid at digit position 1; its three lines of 27
    #   characters are:
    #       _  _  _  _  _  _  _  _
    #      | || || || || || || || |
    #      |_||_||_||_||_||_||_||_|
    # - second: account number 123456789
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _  _  _  _  _  _  _ \n"
        "   | || || || || || || || |\n"
        "   |_||_||_||_||_||_||_||_|\n"
        "\n"
        "    _  _     _  _  _  _  _ \n"
        "  | _| _||_||_ |_   ||_||_|\n"
        "  ||_  _|  | _||_|  ||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result for the first entry is "?00000000 ILL"
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "?00000000 ILL"
    # AND the result for the second entry is "123456789"
    assert lines[1] == "123456789"
    # AND both entries appear in the result file; no entry is dropped
    assert len(lines) == 2


def test_recognition_infra_003_1_s1_no_scan_txt_message_on_stderr_exits_nonzero(
    tmp_path,
):
    # GIVEN the BankOCR image has been built with `docker build -t bankocr .`
    # AND the data folder on the local machine is empty (no scan.txt)
    scan_path = str(tmp_path / "scan.txt")
    result_path = str(tmp_path / "result.txt")

    # WHEN the Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", scan_path, result_path],
        capture_output=True,
        text=True,
    )

    # THEN a message is written to standard error
    assert result.stderr != ""
    # AND the message names the scan file and is not a Python traceback
    assert scan_path in result.stderr
    assert "Traceback" not in result.stderr
    # AND the container exits with a non-zero status
    assert result.returncode != 0
    # AND no result.txt is created in the data folder
    assert not (tmp_path / "result.txt").exists()


def test_recognition_infra_003_1_s2_scan_unreadable_message_on_stderr_exits_nonzero(
    tmp_path,
):
    # GIVEN the BankOCR image has been built with `docker build -t bankocr .`
    # AND the data folder on the local machine contains a scan.txt with read
    # permissions removed
    scan_path = tmp_path / "scan.txt"
    scan_path.write_text("", encoding="utf-8")
    scan_path.chmod(0o000)
    result_path = str(tmp_path / "result.txt")

    # WHEN the Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_path), result_path],
        capture_output=True,
        text=True,
    )

    # THEN a message is written to standard error
    assert result.stderr != ""
    # AND the message names the scan file and is not a Python traceback
    assert str(scan_path) in result.stderr
    assert "Traceback" not in result.stderr
    # AND the container exits with a non-zero status
    assert result.returncode != 0
    # AND no result.txt is created in the data folder
    assert not (tmp_path / "result.txt").exists()


def test_recognition_story_003_s1_scan_file_does_not_exist(tmp_path):
    # GIVEN the data folder on the local machine contains no scan.txt
    scan_path = str(tmp_path / "scan.txt")
    result_path = str(tmp_path / "result.txt")

    # WHEN the Operator runs BankOCR
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", scan_path, result_path],
        capture_output=True,
        text=True,
    )

    # THEN a message is written to standard error
    assert result.stderr != ""
    # AND the message names the scan file and is not a Python traceback
    assert scan_path in result.stderr
    assert "Traceback" not in result.stderr
    # AND the program exits with a non-zero status
    assert result.returncode != 0
    # AND no result file is created
    assert not (tmp_path / "result.txt").exists()


def test_recognition_story_003_s2_scan_file_exists_but_cannot_be_read(tmp_path):
    # GIVEN the data folder on the local machine contains a scan.txt with read
    # permissions removed from the file
    scan_path = tmp_path / "scan.txt"
    scan_path.write_text("", encoding="utf-8")
    scan_path.chmod(0o000)
    result_path = str(tmp_path / "result.txt")

    # WHEN the Operator runs BankOCR
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_path), result_path],
        capture_output=True,
        text=True,
    )

    # THEN a message is written to standard error
    assert result.stderr != ""
    # AND the message names the scan file and is not a Python traceback
    assert str(scan_path) in result.stderr
    assert "Traceback" not in result.stderr
    # AND the program exits with a non-zero status
    assert result.returncode != 0
    # AND no result file is created
    assert not (tmp_path / "result.txt").exists()


def test_reporting_infra_002_1_s1_bankocr_corrects_err_entry_inside_container(
    tmp_path,
):
    # GIVEN the BankOCR image has been built with `docker build -t bankocr .`
    # AND a data folder contains a scan.txt with one entry representing 664371495
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _  _     _  _        _  _ \n"
        "|_ |_ |_| _|  |  ||_||_||_ \n"
        "|_||_|  | _|  |  |  | _| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN data/result.txt on the local machine contains one line: "664371485"
    # with no marker
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines == ["664371485"]
    # AND the container exits with code 0
    assert result.returncode == 0


def test_reporting_story_002_s1_err_entry_with_one_valid_alternative_is_corrected(
    tmp_path,
):
    # GIVEN a scan file with one entry whose three lines of 27 characters are
    # (the number 664371495 which fails the checksum):
    #  _  _     _  _        _  _
    # |_ |_ |_| _|  |  ||_||_||_
    # |_||_|  | _|  |  |  | _| _|
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _  _     _  _        _  _ \n"
        "|_ |_ |_| _|  |  ||_||_||_ \n"
        "|_||_|  | _|  |  |  | _| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result file contains one line: "664371485" with no marker
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines == ["664371485"]


def test_reporting_story_002_s2_ill_entry_with_one_valid_alternative_is_corrected(
    tmp_path,
):
    # GIVEN a scan file with one entry whose three lines of 27 characters are
    # (digit position 9 is a 1 missing its bottom pipe; Recognition produces
    # "?23456789" with status ILL):
    #     _  _     _  _  _  _  _
    #   | _| _||_||_ |_   ||_||_|
    #    |_  _|  | _||_|  ||_| _|
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _     _  _  _  _  _ \n"
        "  | _| _||_||_ |_   ||_||_|\n"
        "   |_  _|  | _||_|  ||_| _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result file contains one line: "123456789" with no marker
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines == ["123456789"]


def test_reporting_story_002_s3_ill_entry_with_no_valid_alternative_keeps_ill(
    tmp_path,
):
    # GIVEN a scan file with one entry whose three lines of 27 characters are
    # (digit position 9 is an all-spaces pattern; Recognition produces
    # "?00000000" with status ILL):
    #     _  _  _  _  _  _  _  _
    #    | || || || || || || || |
    #    |_||_||_||_||_||_||_||_|
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _  _  _  _  _  _  _ \n"
        "   | || || || || || || || |\n"
        "   |_||_||_||_||_||_||_||_|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs BankOCR with the scan file
    subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN the result file contains one line: "?00000000 ILL"
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines == ["?00000000 ILL"]


def test_reporting_infra_003_1_s1_bankocr_marks_amb_entry_inside_container(
    tmp_path,
):
    # GIVEN the BankOCR image has been built with `docker build -t bankocr .`
    # AND a data folder contains a scan.txt with one entry representing 490067715:
    #     _  _  _  _  _  _     _
    # |_||_|| || ||_   |  |  ||_
    #   | _||_||_||_|  |  |  | _|
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        "    _  _  _  _  _  _     _ \n"
        "|_||_|| || ||_   |  |  ||_ \n"
        "  | _||_||_||_|  |  |  | _|\n"
        "\n",
        encoding="utf-8",
    )

    # WHEN the Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`
    result = subprocess.run(
        [sys.executable, "-m", "bankocr", str(scan_file), str(result_file)],
        capture_output=True,
        text=True,
    )

    # THEN data/result.txt on the local machine contains one line: "490067715 AMB"
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines == ["490067715 AMB"]
    # AND the container exits with code 0
    assert result.returncode == 0
