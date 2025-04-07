import os
from .base import VMDetector
from .models import VMIndicator

class WindowsVMDetector(VMDetector):
    def check_cpu_info(self):
        cpu_info = self.run_command("wmic cpu get manufacturer, name, caption")
        cpu_indicators = self.config.get('cpu_indicators', [])
        if any(x in cpu_info for x in cpu_indicators):
            return True, VMIndicator("CPU manufacturer indicates virtualization")
        return False, None

    def check_system_model(self):
        system_info = self.run_command("wmic computersystem get manufacturer, model")
        vm_vendors = self.config.get('vm_vendors', [])
        for vendor in vm_vendors:
            if vendor in system_info:
                return True, VMIndicator(f"System manufacturer indicates VM: {vendor}")
        return False, None

    def check_mac_address(self):
        ipconfig = self.run_command("ipconfig /all")
        mac_prefixes = self.config.get('mac_prefixes', [])
        for prefix in mac_prefixes:
            if prefix.lower() in ipconfig:
                return True, VMIndicator(f"VM MAC prefix detected: {prefix}")
        return False, None

    def check_processes(self):
        processes = self.run_command("tasklist")
        vm_processes = self.config.get('processes', [])
        for proc in vm_processes:
            if proc.lower() in processes:
                return True, VMIndicator(f"VM process detected: {proc}", high_confidence=True)
        return False, None

    def check_specific_files(self):
        vm_files = self.config.get('vm_files', [])
        for file in vm_files:
            if os.path.exists(file):
                return True, VMIndicator(f"VM file detected: {file}")
        return False, None

    def additional_os_specific_checks(self):
        vm_services = self.config.get('service_checks', [])
        for service in vm_services:
            service_output = self.run_command(f"sc query {service}")
            if service_output and "running" in service_output:
                return True, VMIndicator(f"VM service running: {service}", high_confidence=True)
        
        return False, None
