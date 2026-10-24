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
    # GIVEN a data folder contains scan.txt with one entry representing 664371495
    # AND no result.txt exists in the data folder
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _  _     _  _        _  _ \n"
        "|_ |_ |_| _|  |  ||_||_||_ \n"
        "|_||_|  | _|  |  |  | _| _|\n"
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
    # AND data/result.txt contains "664371495 ERR"
    assert result_file.read_text(encoding="utf-8").splitlines() == ["664371495 ERR"]


def test_validation_infra_001_3_s1_err_entries_produce_no_diagnostic_messages(
    tmp_path,
):
    # GIVEN a scan file containing 345882865 and 664371495
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _     _  _        _  _ \n"
        "|_ |_ |_| _|  |  ||_||_||_ \n"
        "|_||_|  | _|  |  |  | _| _|\n"
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
    # GIVEN a scan file with two entries: 345882865 and 664371495
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
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

    # THEN the result file has two lines
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    # AND line 1 is "345882865" with no marker
    assert lines[0] == "345882865"
    # AND line 2 is "664371495 ERR"
    assert lines[1] == "664371495 ERR"


def test_reporting_infra_001_1_s1_reporting_runs_inside_the_container(tmp_path):
    # GIVEN a data folder contains a scan.txt with two entries
    # representing 345882865 and 664371495
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _     _  _        _  _ \n"
        "|_ |_ |_| _|  |  ||_||_||_ \n"
        "|_||_|  | _|  |  |  | _| _|\n"
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
    # AND data/result.txt contains "345882865" on line 1 and "664371495 ERR" on line 2
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "345882865"
    assert lines[1] == "664371495 ERR"
    # AND the container exits with code 0
    assert result.returncode == 0


def test_reporting_infra_001_2_s1_result_file_written_to_mounted_data_folder(
    tmp_path,
):
    # GIVEN a data folder contains scan.txt with two entries
    # representing 345882865 and 664371495
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _     _  _        _  _ \n"
        "|_ |_ |_| _|  |  ||_||_||_ \n"
        "|_||_|  | _|  |  |  | _| _|\n"
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
    # AND data/result.txt contains "345882865" on line 1 and "664371495 ERR" on line 2
    lines = result_file.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "345882865"
    assert lines[1] == "664371495 ERR"


def test_reporting_infra_001_3_s1_err_entries_produce_no_diagnostic_messages(
    tmp_path,
):
    # GIVEN a scan file containing 345882865 and 664371495
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _     _  _        _  _ \n"
        "|_ |_ |_| _|  |  ||_||_||_ \n"
        "|_||_|  | _|  |  |  | _| _|\n"
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
    # GIVEN a scan file with three entries: 345882865, 664371495 and 123456789
    scan_file = tmp_path / "scan.txt"
    result_file = tmp_path / "result.txt"
    scan_file.write_text(
        " _     _  _  _  _  _  _  _ \n"
        " _||_||_ |_||_| _||_||_ |_ \n"
        " _|  | _||_||_||_ |_||_| _|\n"
        "\n"
        " _  _     _  _        _  _ \n"
        "|_ |_ |_| _|  |  ||_||_||_ \n"
        "|_||_|  | _|  |  |  | _| _|\n"
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
    # AND line 2 is "664371495 ERR"
    assert lines[1] == "664371495 ERR"
    # AND line 3 is "123456789" with no marker
    assert lines[2] == "123456789"
