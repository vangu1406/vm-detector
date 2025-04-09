from src.vm_detector import VMIndicator
from unittest.mock import patch
from .conftest import _TestDetector


def test_vm_indicator():
    indicator = VMIndicator("test evidence", True)
    assert indicator.evidence == "test evidence"
    assert indicator.high_confidence == True


def test_run_command():
    with patch("subprocess.check_output", return_value="test output"):
        detector = _TestDetector()
        result = detector.run_command("test command")
        assert result == "test output"


def test_run_command_failure():
    with patch("subprocess.check_output", side_effect=Exception("Command failed")):
        detector = _TestDetector()
        result = detector.run_command("test command")
        assert result == ""
