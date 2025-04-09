#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
import yaml
from pathlib import Path
from abc import ABC, abstractmethod
from .models import VMIndicator


class VMDetector(ABC):
    def __init__(self):
        self.os_type = platform.system()
        self.vm_indicators = []
        self.config = self._load_config()

    def _load_config(self):
        try:
            config_path = Path(__file__).parent / "config" / "vm_detector_config.yaml"
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                return config[self.os_type.lower()]
        except FileNotFoundError:
            print("Configuration file 'vm_detector_config.yaml' not found.")
            sys.exit(1)
        except KeyError:
            print(f"System configuration for '{self.os_type}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)

    def run_command(self, command):
        try:
            output = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True
            )
            return output.lower()
        except:
            return ""

    @abstractmethod
    def check_cpu_info(self):
        pass

    @abstractmethod
    def check_system_model(self):
        pass

    @abstractmethod
    def check_mac_address(self):
        pass

    @abstractmethod
    def check_processes(self):
        pass

    @abstractmethod
    def check_specific_files(self):
        pass

    @abstractmethod
    def additional_os_specific_checks(self):
        pass

    def detect(self):
        checks = [
            self.check_cpu_info(),
            self.check_system_model(),
            self.check_mac_address(),
            self.check_processes(),
            self.check_specific_files(),
            self.additional_os_specific_checks(),
        ]

        positive_results = [
            indicator for result, indicator in checks if result and indicator
        ]
        has_high_confidence = any(
            indicator.high_confidence for indicator in positive_results
        )

        self.vm_indicators = positive_results
        return self._generate_result(positive_results, has_high_confidence)

    def _generate_result(self, positive_results, has_high_confidence):
        if len(positive_results) >= 2 or has_high_confidence:
            print("Warning: VM detected!")
            print("Indicators found:")
            for indicator in positive_results:
                confidence = "(High Confidence)" if indicator.high_confidence else ""
                print(f"- {indicator.evidence} {confidence}")
            return True
        elif len(positive_results) == 1:
            print("RESULT: possible virtual machine, but only one evidence found.")
            print(f"- {positive_results[0].evidence}")
            print(
                "This could be a false positive. It is recommended to check using other methods."
            )
            return False
        else:
            print(
                "RESULT: No virtual machines detected. This appears to be bare metal system."
            )
            return False
