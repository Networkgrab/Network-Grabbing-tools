# Networkgrabbing

![Project Logo](https://github.com/Networkgrab/Networkgrabbing/blob/main/logo.png)

## Description

Network grabbing is the process of obtaining network-related data. Suppose that you are attempting to learn about a new city. Start by consulting a map, speaking with locals, or taking a self-guided walk around the streets. Network grabbing is similar in that it gathers information about the connections between computers and other devices. This can include the types of devices on the network, their connections, and the software they are using. To grasp how everything is connected, it's like making a map of the digital world.

### Key Features

- **Host Grabbing**: Identifies active devices on the network using techniques such as ICMP Echo requests and TCP pings.
- **Port Grabbing**: Detects open ports on discovered hosts to understand the services available on each device.
- **Service Detection**: Determines the services and their versions running on identified open ports.
- **Operating System Fingerprinting**: Attempts to identify the operating system of each discovered host using various heuristics.
- **Vulnerability Grabbing**: Enables you to find possible security flaws and vulnerabilities in target systems or networks.
- **Mitigation**: Provides mitigation recommendations when a vulnerability is identified.

## How to Use Network Grabbing

Using these scripts is very easy, though it assumes you have nmap already installed, as it is the primary dependency required. This tool supports both Windows and Linux, making it cross-platform.

## Dependencies

- nmap/python-nmap
- Python 3
- subprocess
- socket
- threading
- pyfiglet
- colorama
- os
- scapy
- base64
- getpass
- re
- xml.etree.ElementTree

## Installation

### For Linux:

1. **Install Python 3**:
   Ensure Python 3 is installed on your system. If not, download and install it from the [official Python website](https://www.python.org/downloads/).

2. **Install nmap**:
   Install nmap using your package manager. For example, on Debian/Ubuntu, use:
   ```sh
   sudo apt-get install nmap

3. **Clone the Repository**
   Open a terminal, navigate to your desired directory, and run:
   ```sh
   git clone https://github.com/Networkgrab/Networkgrabbing.git

4. **Install Dependencies**
    Navigate to the cloned repository directory:
    ```sh
    cd Networkgrabbing

   Install the required dependencies using pip:
   ```sh
   python3 -m pip install -r requirements.txt

## for Window

### Install Python 3
1. Download the latest version of Python 3 from the [official website](https://www.python.org/).
2. During installation, make sure to check the box that says "Add Python to PATH" to make Python accessible from the command line.

### Install Git
1. If you haven't already, download and install Git from the [official website](https://git-scm.com/).
2. During installation, ensure that Git is added to your system PATH.

### Install nmap
1. Download the nmap installer for Windows from the [official website](https://nmap.org/download.html).
2. Follow the installation instructions provided by the installer.
3. Note down the installation directory of nmap (e.g., `C:\Program Files (x86)\Nmap`).

### Clone the Repository and Install Dependencies
1. Open Command Prompt (cmd) or PowerShell.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command to clone the repository:

    ```sh
    git clone https://github.com/Networkgrab/Networkgrabbing.git
4. Navigate to the cloned repository directory:

   ```sh
   cd Networkgrabbing
5. Install the required dependencies using pip:

   ```sh
   pip install -r requirements.txt


### Usage

### Navigate to the Networkgrabbing Directory And Execute the Script
1. Open a terminal or Command Prompt.
2. Navigate to the Networkgrabbing directory within the cloned repository:

    ```sh
    cd Networkgrabbing

3. Run the following command:

    ```sh
    python3 networkgrabbing.py

## Contributing

Guidelines for contributing to the project:

- Report bugs
- Suggest enhancements
- Submit pull requests

## Team Members

- [Avart raj Vishwakarma]
- [Khushi Kumari]
- [Deepak Singh]
- [Mansi Dubey]

## License

Information about the project's license and any terms of use.
