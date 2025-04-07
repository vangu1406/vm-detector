import platform
from .windows_detector import WindowsVMDetector
from .linux_detector import LinuxVMDetector

def create_detector():

    os_type = platform.system()
    if os_type == "Windows":
        return WindowsVMDetector()
    elif os_type == "Linux":
        return LinuxVMDetector()
    else:
        raise RuntimeError(f"OS not supported: {os_type}")
