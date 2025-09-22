CoreGuardian 🛡️

A Linux kernel module testing framework for detecting crashes, panics, and vulnerabilities.

📌 Overview

CoreGuardian is a lightweight framework designed to test the stability and security of the Linux kernel by loading custom kernel modules that intentionally trigger faults or stress the system.

The project helps developers and security researchers observe kernel behavior, identify vulnerabilities, and safely experiment with kernel-level code inside a virtualized environment.

✨ Features

🧩 Custom Kernel Modules – Create and load .ko files to test different kernel operations.

⚡ Fault Injection – Trigger edge cases to detect improper memory handling or panics.

🔍 Crash Detection – Monitor system logs (dmesg) for kernel oops or crashes.

🖥️ VM Safe Environment – Designed for testing inside virtual machines like VMware.

🌱 Educational Resource – Great for learning Linux kernel internals and low-level programming.

🛠️ Tech Stack
Component	Technology Used
Language	C (Kernel Module Development)
Kernel	Linux Kernel (Tested on Ubuntu)
Virtualization	VMware Workstation
Tools	GCC, Make, Git
📂 Project Structure
CoreGuardian/
│
├── kernel_test_module/
│   ├── oops_demo.c          # Core faulty kernel module source code
│   ├── Makefile             # Build instructions for the module
│   └── README.md            # Module-level documentation
│
├── scripts/                 # Helper scripts for testing and logging
│
└── docs/                     # Additional documentation

🚀 Installation & Setup
1. Clone the Repository
git clone https://github.com/<your-username>/CoreGuardian.git
cd CoreGuardian/kernel_test_module

2. Build the Kernel Module

Ensure you have Linux kernel headers installed:

sudo apt update
sudo apt install build-essential linux-headers-$(uname -r)


Compile the module:

make


This will generate:

oops_demo.ko

3. Insert the Module into the Kernel

⚠️ Warning: Only test inside a virtual machine to prevent damaging your host system.

sudo insmod oops_demo.ko


If successful, check logs:

dmesg | tail

4. Remove the Module
sudo rmmod oops_demo

⚙️ Implementation Details

The oops_demo.c module is designed to intentionally trigger a fault in the kernel to test how the system handles abnormal behavior.

Key Steps in Implementation

Module Initialization (init_module)

The module is loaded using insmod.

Registers itself with the kernel logging system.

Fault Triggering

The module deliberately performs invalid memory access or other unsafe operations, which should cause a kernel oops.

This helps researchers observe how the kernel reacts to unsafe code.

Cleanup (cleanup_module)

Proper cleanup is done to remove traces after testing using rmmod.

📊 Example Log Output

Example output after inserting the module:

[  120.567890] CoreGuardian: Loading faulty module...
[  120.567912] BUG: unable to handle kernel NULL pointer dereference at 00000000
[  120.567933] Oops: 0002 [#1] SMP
[  120.567950] CoreGuardian: Test complete - kernel crash successfully simulated.

🧪 Testing Workflow

Launch your VMware Linux VM.

Build and load the kernel module.

Use dmesg or /var/log/kern.log to monitor crashes.

Document the observed behavior for security research or educational purposes.

🌐 Future Enhancements

Add automated logging scripts to record kernel behavior.

Provide a dashboard for visualizing crash data.

Include more fault types like memory leaks and race conditions.

Add GitHub Actions for automated module build testing.

📜 License

This project is licensed under the MIT License – you are free to use, modify, and distribute it for educational or research purposes.

🙌 Acknowledgements

Linux Kernel Documentation – invaluable resource for module development.

Open-source community for tools like GCC and VMware Workstation.

Final Note

CoreGuardian is meant strictly for educational and research purposes.
Never load faulty kernel modules on a production system — always use a virtual machine or test environment.
