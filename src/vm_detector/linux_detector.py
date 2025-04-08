import os
import re
from .base import VMDetector
from .models import VMIndicator

class LinuxVMDetector(VMDetector):
    def check_cpu_info(self):
        if os.path.exists("/proc/cpuinfo"):
            try:
                with open("/proc/cpuinfo", "r") as f:
                    cpu_info = f.read().lower()
                    if re.search(r"flags\s*:.*\bhypervisor\b", cpu_info):
                        return True, VMIndicator(
                            "Flag 'hypervisor' in /proc/cpuinfo",
                            high_confidence=True
                        )
            except:
                pass
        return False, None

    def check_system_model(self):
        model_files = self.config.get('model_files', [])
        vm_indicators = self.config.get('vm_vendors', [])
        
        for file in model_files:
            if os.path.exists(file):
                try:
                    with open(file, "r") as f:
                        content = f.read().lower()
                        if any(x in content for x in vm_indicators):
                            return True, VMIndicator(f"File {file} indicates VM: {content.strip()}")
                except:
                    pass
        return False, None

    def check_mac_address(self):
        net_info = self.run_command("ip link 2>/dev/null")
        mac_prefixes = self.config.get('mac_prefixes', [])
        for prefix in mac_prefixes:
            if prefix.lower() in net_info:
                return True, VMIndicator(f"VM MAC prefix detected: {prefix}")
        return False, None

    def check_processes(self):
        vm_processes = self.config.get('processes', [])
        for proc in vm_processes:
            result = self.run_command(f"pgrep -f {proc}")
            if result.strip():
                return True, VMIndicator(f"VM process detected: {proc}", high_confidence=True)
        return False, None

    def check_specific_files(self):
        if os.path.exists("/proc/modules"):
            try:
                with open("/proc/modules", "r") as f:
                    content = f.read().lower()
                    vm_modules = self.config.get('kernel_modules', [])
                    for module in vm_modules:
                        if module in content:
                            return True, VMIndicator(
                                f"VM kernel module detected: {module}",
                                high_confidence=True
                            )
            except:
                pass
        return False, None

    def additional_os_specific_checks(self):
        lscpu_output = self.run_command("lscpu 2>/dev/null")
        if "hypervisor vendor" in lscpu_output:
            match = re.search(r"hypervisor vendor:\s*(\w+)", lscpu_output)
            if match:
                return True, VMIndicator(
                    f"lscpu indicates hypervisor: {match.group(1)}",
                    high_confidence=True
                )
            return True, VMIndicator("lscpu indicates hypervisor", high_confidence=True)
        
        return False, None
