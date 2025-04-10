### vm-detector

vm-detector is a module to detect the presence of virtual machines on **Linux** and **Windows** systems.

## Features

Detection of indicators related to:

- CPU and Hypervisor flags
- System manufacturer
- Known VM processes
- VM-related files and kernel modules
- Active services associated with virtual machines

## Installation
You can install vm-detector locally using one of the following methods:

```
pip install .
```

or using the Makefile:
```
make install
```

For development setup (testing, linting etc.):
```
make dev-setup
```

## Usage

### Command line
Once installed, you can run ```vm-detector``` command from the terminal to check for virtualization indicators:

```
$ vm-detector
Warning: VM detected!
Indicators found:
- Flag 'hypervisor' in /proc/cpuinfo (High Confidence)
- File /sys/devices/virtual/dmi/id/product_name indicates VM: vmware virtual platform 
- VM MAC prefix detected: 00:0c:29 
- VM process detected: vmtoolsd (High Confidence)
- VM kernel module detected: vmw_balloon (High Confidence)
- lscpu indicates hypervisor: vmware (High Confidence)
```

### Python

You can also integrate the module directly into your own project by importing ```create_detector``` and using the ```detect()``` method:

```py
from vm_detector import create_detector

detector = create_detector()
detector.detect()
```

The ```detect()``` method runs multiple checks to identify virtual machine indicators, such as CPU flags, system model, processes and more. Each check returns a tuple ```(result: bool, indicator: VMIndicator())```, where:

- ```result``` is True if the check was successful;
- ```indicator``` is an instance of ```VMIndicator()``` dataclass.

Here's an example:

```py
from vm_detector import create_detector

detector = create_detector()
detector.check_processes()
(True, VMIndicator(evidence='VM process detected: vmtoolsd', high_confidence=True))
```

## LICENSE
This project is licensed under the **GNU GPL v3** - see the [LICENSE](https://github.com/vangu1406/vm-detector/blob/main/LICENSE) file for details. 
