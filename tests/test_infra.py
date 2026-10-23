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
