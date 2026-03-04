# PyShark DNS Extractor 🔍🐍

A simple yet powerful Python script to extract DNS queries from Wireshark (.pcap / .pcapng) capture files using PyShark.

It shows:
- Source IP of the device asking the query
- Queried domain name
- Query type (1 = A / IPv4, 28 = AAAA / IPv6, etc.)
- Packet number for reference
- DNS server IP (detected from the first query's destination)
- Removes duplicates for clean output
- Shows total packets processed and unique queries found

### Features
- Supports .pcap and .pcapng files
- Filters only DNS queries (not responses)
- Handles both IPv4 and IPv6
- Removes duplicate queries (same source + same domain shown only once)
- Detects DNS server IP automatically
- Clean table-style output with summary

### Requirements
- Python 3
- PyShark (`pip install pyshark`)
- Wireshark / tshark installed (`sudo apt install tshark -y` on Kali/Debian)

### Recommended Setup
Use a virtual environment for clean installation:

```bash
python3 -m venv venv
source venv/bin/activate
pip install pyshark

### How to Use
Run the script by passing your .pcap file path:
Bashpython3 dns_analyzer.py /path/to/your_capture.pcap
Or edit the script file and change the file_path variable inside the __main__ block to hardcode your file.

### Sample Output
textPyShark DNS Query Extractor 🔍
==================================================
DNS Server IP: 192.168.114.2

Pkt #  Src IP            Domain Name                                        Type
--------------------------------------------------------------------------------
1      192.168.114.131   google.com                                         1
5      192.168.114.131   youtube.com                                        28
13     192.168.114.131   www.neduet.edu.pk                                  1
17     192.168.114.131   www.geeksforgeeks.org                              1
21     192.168.114.131   chatgpt.com                                        28
...

Total DNS packets processed: 580
Unique DNS queries found: 292

### How It Works
-Opens the .pcap file with PyShark and filters only DNS queries (dns.flags.response == 0).
-Extracts source IP, domain name (dns.qry_name), and query type (dns.qry_type).
-Uses a set to avoid duplicate entries (same source IP + same domain).
-Detects DNS server IP from the destination of the first query.
-Prints a neat table + summary stats at the end.

### Quick DNS Reminder
DNS Query → Your device asks: “What is the IP of google.com?”
DNS Response → DNS server replies with the IP address (or error)
Type 1 = A record (IPv4)
Type 28 = AAAA record (IPv6)
