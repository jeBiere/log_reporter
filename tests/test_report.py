import tempfile
import os
import pytest
from report import process_logs, generate_average_report

def create_temp_log_file(lines):
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    temp_file.writelines(line + '\n' for line in lines)
    temp_file.flush()
    temp_file.close()
    return temp_file.name

def test_process_logs_basic():
    logs = [
        '{"url": "/api/a", "response_time": 0.1}',
        '{"url": "/api/a", "response_time": 0.3}',
        '{"url": "/api/b", "response_time": 0.2}'
    ]
    file_path = create_temp_log_file(logs)
    stats = process_logs([file_path])
    os.unlink(file_path)

    assert stats["/api/a"][0] == 2
    assert abs(stats["/api/a"][1] - 0.4) < 1e-6
    assert stats["/api/b"][0] == 1
    assert abs(stats["/api/b"][1] - 0.2) < 1e-6

def test_process_logs_with_invalid_lines():
    logs = [
        '{"url": "/api/a", "response_time": 0.1}',
        'invalid json line',
        '{"url": "/api/b", "response_time": 0.2}',
        '{"url": "/api/a"}' 
    ]
    file_path = create_temp_log_file(logs)
    stats = process_logs([file_path])
    os.unlink(file_path)

    assert stats["/api/a"][0] == 1
    assert abs(stats["/api/a"][1] - 0.1) < 1e-6
    assert stats["/api/b"][0] == 1
    assert abs(stats["/api/b"][1] - 0.2) < 1e-6

def test_generate_average_report_output():
    stats = {
        "/api/a": [2, 0.4],
        "/api/b": [1, 0.2],
    }
    report = generate_average_report(stats)
    assert "/api/a" in report
    assert "/api/b" in report
    assert "2" in report
    assert "0.2" in report or "0.200" in report

def test_process_logs_empty_file():
    file_path = create_temp_log_file([])
    stats = process_logs([file_path])
    os.unlink(file_path)
    assert stats == {}

def test_process_logs_nonexistent_file():
    fake_path = "nonexistent_file.log"
    with pytest.raises(FileNotFoundError):
        process_logs([fake_path])

def test_process_logs_large_file():
    lines = ['{"url": "/api/large", "response_time": 0.1}'] * 10000
    file_path = create_temp_log_file(lines)
    stats = process_logs([file_path])
    os.unlink(file_path)

    assert stats["/api/large"][0] == 10000
    assert abs(stats["/api/large"][1] - 1000.0) < 1e-6

def test_generate_average_report_empty_stats():
    report = generate_average_report({})
    assert "Endpoint" in report
    lines = report.strip().split('\n')
    assert len(lines) == 2
