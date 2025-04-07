import pytest
from unittest.mock import patch
from src.vm_detector import WindowsVMDetector, LinuxVMDetector

def test_windows_detect_vm(windows_detector):
    with patch.object(windows_detector, 'run_command') as mock_run:
        mock_run.side_effect = [
            'vmware cpu',  # cpu_info
            'manufacturer: vmware',  # system_model
            '00:0c:29:12:34:56',  # mac_address
            'vmtoolsd.exe',  # processes
            'running'  # service check
        ]
        assert windows_detector.detect() == True

def test_linux_detect_no_vm(linux_detector):
    with patch.object(linux_detector, 'run_command') as mock_run:
        mock_run.return_value = ''
        with patch('os.path.exists', return_value=False):
            assert linux_detector.detect() == False 
