##   Port Scanner Project
###  Description

This is a simple Port Scanner tool built in Python that allows you to scan a network for live hosts and open ports. The script can automatically identify the local network and scan for common open ports on machines connected to the same network. It also supports multi-threading to speed up the scanning process.

##   Features:
### Scans a range of IP addresses on a local network.
### Identifies common open ports (like 22, 80, 443, etc.).
### Retrieves banners for open ports (for service identification).
### Supports multi-threading for faster scanning.
### Can automatically determine the local network and scan for IP addresses.

##   Installation
### Prerequisites
### To run this project, you need the following:

Python 3 or higher installed.
Some Python libraries:
socket
subprocess
threading
ipaddress
logging
re
You can install any missing dependencies using pip:

bash
Copy code
pip install <package-name>
Setup
Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/your-username/port-scanner.git
Navigate to the project directory:

bash
Copy code
cd port-scanner
Run the Python script:

bash
Copy code
python scanner.py
Usage
Once the script is running, it will automatically:

Detect the local network (using your machine’s IP).
Discover live hosts within the network.
Scan common ports for each live host.
Display open ports along with service banners, if available.
Example output:

bash
Copy code
Starting scan on network: 192.168.1.0/24 from port 20 to 100
[+] 192.168.1.1 is live
[+] Port 80 is OPEN on 192.168.1.1
[+] Port 443 is OPEN on 192.168.1.1
[-] Port 21 is CLOSED on 192.168.1.2
Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

How to Contribute:
Fork the repository.
Create a new branch for your feature or fix.
Make your changes and commit them.
Push to your forked repository.
Create a pull request describing your changes.
License
This project is licensed under the MIT License - see the LICENSE file for details.
