import subprocess
import sys
from pathlib import Path

BASE_COMMAND = [sys.executable, "main.py"]

def run_cli(args):
    return subprocess.run(
        BASE_COMMAND + args,
        capture_output=True,
        text=True
    )

def test_no_arguments():
    result = run_cli([])
    assert result.returncode != 0
    assert "usage:" in result.stderr.lower()

def test_invalid_report_type():
    result = run_cli(["--report", "invalid", "--file", "tests/data/example1.log"])
    assert result.returncode != 0
    assert "invalid choice" in result.stderr.lower()

def test_nonexistent_file():
    result = run_cli(["--report", "average", "--file", "not_found.log"])
    assert result.returncode == 1
    assert "The following files do not exist" in result.stdout
    assert "No valid log files found." in result.stdout


def test_invalid_json_file(tmp_path):
    bad_file = tmp_path / "bad.log"
    bad_file.write_text("this is not json\njust text")

    result = run_cli(["--report", "average", "--file", str(bad_file)])
    assert result.returncode == 0
    assert "Endpoint" in result.stdout

def test_valid_input_file():
    valid_file = Path("tests/data/example1.log")
    result = run_cli(["--report", "average", "--file", str(valid_file)])
    assert result.returncode == 0
    assert "Endpoint" in result.stdout
    assert "/api/homeworks/" in result.stdout or "/api/context/" in result.stdout

def test_unrecognized_argument():
    result = run_cli(["--flie", "some.log", "--report", "average"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()

