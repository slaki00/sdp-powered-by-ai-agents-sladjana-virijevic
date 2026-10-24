"""CLI Entry Point tests for RECOGNITION-STORY-003 (file-error handling)."""

import subprocess
import sys


def test_recognition_be_003_1_s1_scan_file_not_found_message_on_stderr(tmp_path):
    # GIVEN the input file path passed to the CLI Entry Point points to a file
    # that does not exist
    scan_path = str(tmp_path / "scan.txt")
    result_path = str(tmp_path / "result.txt")

    # WHEN the CLI Entry Point attempts to open the scan file
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
    # AND the CLI Entry Point exits with a non-zero status
    assert result.returncode != 0
    # AND no result file is created
    assert not (tmp_path / "result.txt").exists()


def test_recognition_be_003_1_s2_scan_file_unreadable_message_on_stderr(tmp_path):
    # GIVEN the input file path passed to the CLI Entry Point points to a file
    # that exists but has read permissions removed
    scan_path = tmp_path / "scan.txt"
    scan_path.write_text("", encoding="utf-8")
    scan_path.chmod(0o000)
    result_path = str(tmp_path / "result.txt")

    # WHEN the CLI Entry Point attempts to open the scan file
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
    # AND the CLI Entry Point exits with a non-zero status
    assert result.returncode != 0
    # AND no result file is created
    assert not (tmp_path / "result.txt").exists()
