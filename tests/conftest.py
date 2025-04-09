import pytest
from unittest.mock import patch
from src.vm_detector import VMDetector, WindowsVMDetector, LinuxVMDetector


# testing helper class
class _TestDetector(VMDetector):
    def check_cpu_info(self):
        pass

    def check_system_model(self):
        pass

    def check_mac_address(self):
        pass

    def check_processes(self):
        pass

    def check_specific_files(self):
        pass

    def additional_os_specific_checks(self):
        pass


@pytest.fixture
def windows_detector():
    with patch("platform.system", return_value="Windows"):
        with patch("src.vm_detector.base.VMDetector._load_config") as mock_config:
            mock_config.return_value = {
                "cpu_indicators": ["vmware"],
                "vm_vendors": ["vmware", "virtualbox"],
                "mac_prefixes": ["00:0c:29"],
                "processes": ["vmtoolsd.exe"],
                "vm_files": ["C:\\Windows\\System32\\vmGuestLib.dll"],
                "service_checks": ["vmtools"],
            }
            return WindowsVMDetector()


@pytest.fixture
def linux_detector():
    with patch("platform.system", return_value="Linux"):
        with patch("src.vm_detector.base.VMDetector._load_config") as mock_config:
            mock_config.return_value = {
                "model_files": ["/sys/class/dmi/id/product_name"],
                "vm_vendors": ["vmware", "virtualbox"],
                "mac_prefixes": ["00:0c:29"],
                "processes": ["vmtoolsd"],
                "kernel_modules": ["vmware"],
            }
            return LinuxVMDetector()
