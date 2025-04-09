import pytest
from unittest.mock import patch, mock_open


def test_linux_check_cpu_info(linux_detector):
    mock_cpuinfo = (
        "processor : 0\nflags : fpu vme de pse tsc msr pae mce cx8 hypervisor"
    )
    with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
        with patch("os.path.exists", return_value=True):
            result, indicator = linux_detector.check_cpu_info()
            assert result == True
            assert "hypervisor" in indicator.evidence.lower()


def test_linux_check_system_model(linux_detector):
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="VMware")):
            result, indicator = linux_detector.check_system_model()
            assert result == True
            assert "indicates VM" in indicator.evidence


def test_linux_check_processes(linux_detector):
    with patch.object(linux_detector, "run_command", return_value="vmtoolsd"):
        result, indicator = linux_detector.check_processes()
        assert result == True
        assert indicator.high_confidence == True
