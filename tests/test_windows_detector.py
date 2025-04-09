import pytest
from unittest.mock import patch


def test_windows_check_cpu_info(windows_detector):
    with patch.object(windows_detector, "run_command", return_value="vmware cpu"):
        result, indicator = windows_detector.check_cpu_info()
        assert result == True
        assert "CPU manufacturer" in indicator.evidence


def test_windows_check_system_model(windows_detector):
    with patch.object(
        windows_detector, "run_command", return_value="manufacturer: vmware"
    ):
        result, indicator = windows_detector.check_system_model()
        assert result == True
        assert "System manufacturer" in indicator.evidence


def test_windows_check_mac_address(windows_detector):
    with patch.object(
        windows_detector, "run_command", return_value="00:0c:29:12:34:56"
    ):
        result, indicator = windows_detector.check_mac_address()
        assert result == True
        assert "VM MAC prefix detected" in indicator.evidence


def test_windows_check_processes(windows_detector):
    with patch.object(windows_detector, "run_command", return_value="vmtoolsd.exe"):
        result, indicator = windows_detector.check_processes()
        assert result == True
        assert indicator.high_confidence == True
