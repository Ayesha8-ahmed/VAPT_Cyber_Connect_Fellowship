# Network Traffic Basics
## Overview
The Network Traffic Basics room on TryHackMe introduces the concept of **Network Traffic Analysis (NTA)** and explains:

- What NTA is  
- Why it is important  
- What can be observed in network traffic  
- Network sources and flows  
- How to capture and analyze traffic  
- Practical packet inspection scenarios  

---
## Task 1 – Introduction to Network Traffic Analysis

### What is Network Traffic Analysis?
Network Traffic Analysis (NTA) is the process of:

- **Capturing**  
- **Inspecting**  
- **Analyzing**  

data as it flows across a network.

**Goal of NTA:**

- Complete visibility of communications  
- Insight into internal and external traffic  
- Detection of abnormal or malicious behavior  

 **Important:** NTA is **NOT just Wireshark**.  
It includes:

- Log correlation  
- Deep Packet Inspection (DPI)  
- Flow statistics (NetFlow/IPFIX)  
- Security analysis  

### Learning Objectives
After completing this room, we understand:

- What NTA is  
- What can be observed  
- How to observe traffic  
- Typical traffic sources and flows  

---

## Task 2 – Purpose of Network Traffic Analysis

### Scenario: DNS Tunneling & Beaconing
A SOC analyst notices abnormal DNS activity from:

- **Host:** WIN-016  
- **IP:** 192.168.1.16
Firewall logs show repeated DNS queries to:
aj39skdm.malicious-tld.com
msd91azx.malicious-tld.com
cmd01.malicious-tld.com
Some queries use: `QTYPE=TXT`

### What Do DNS Logs Show?
From logs we can extract:

- Query name  
- Query type  
- Source IP  
- Destination IP  
- Timestamp  

**But logs do NOT show:** actual DNS payload content

### Packet Inspection Reveals:
TXT record:
TXT: "SSBsb3ZlIHlvdXIgY3VyaW91c2l0eQ=="


This is Base64 encoded.  
Decoded message: `I love your curiosity`  

**Demonstrates:** attackers sending C2 commands via DNS TXT records.

 **Answer:**  
**Technique:** DNS Tunneling

### Why Do We Analyze Network Traffic?
Network Traffic Analysis helps to:

- Monitor network performance  
- Detect abnormalities  
- Identify exfiltration attempts  
- Detect malicious downloads  
- Reconstruct attacks  
- Validate security alerts  

---

## Task 3 – What Can We Observe?

Network traffic can be analyzed using the **TCP/IP model**.

### Application Layer
Example: HTTP traffic

**HTTP Request:**

GET /downloads/suspicious_package.zip HTTP/1.1


**HTTP Response:**
<img width="835" height="226" alt="Screenshot 2026-02-21 223401" src="https://github.com/user-attachments/assets/948959d8-7daf-4e44-9f54-681180b3785d" />

Content-Length: 10485760
Content-Disposition: attachment; filename="suspicious_package.zip"


**Question:** What is the size of the ZIP attachment?  
 10485760 bytes  

Logs show:
- File name  
- Response code  
- File size  

**But logs do NOT show:** actual file content  
For that → **full packet capture** is needed

---

### Transport Layer (TCP)
Example firewall logs:


flags=SYN
flags=SYN,ACK


Shows the **TCP 3-way handshake**.  

**In Wireshark:**

- SYN  
- SYN-ACK  
- ACK  

Later:


Seq=34567232


Large jump in sequence number → suspicious  

**Question:** Which field in TCP header helps detect session hijacking?  
 Sequence number

---

### Internet Layer (IP)
Fragmentation example:

- Overlapping fragment offsets can:  
  - Evade IDS  
  - Cause reassembly confusion  

**Question:** Which attack do attackers use to evade IDS?  
 Fragmentation attack

---

### Link Layer
ARP spoofing example:

- Attacker replies with fake MAC address:


192.168.1.10 is at aa:bb:cc:dd:ee:ff

Used for **Man-in-the-Middle (MITM)**

---

## Task 4 – Network Traffic Sources & Flows

### Sources

**Intermediary Devices**  
- Firewalls  
- Routers  
- Switches  
- IDS/IPS  
Generate **less traffic**  

** Endpoint Devices**  
- Workstations  
- Servers  
- IoT & Mobile devices  
Generate **most traffic**  

**Question:** Which category generates most traffic?  
 Endpoint

---

### Flows
**North-South Traffic:**  
Traffic between LAN and WAN  
Examples: HTTPS, DNS, SSH, VPN  

**East-West Traffic:**  
Internal LAN traffic  
Important for detecting: Lateral movement, internal compromise  

**SMB Flow Question:**  
Before SMB session establishment, which service is contacted first?  
 Kerberos  

**TLS Question:** What does TLS stand for?  
 Transport Layer Security  

---

## Task 5 – How Can We Observe Network Traffic?

Traffic can be observed using:

### Logs
- Syslog  
- Apache logs  
- Windows Event Logs  

**Logs show:** metadata, not full packets  

---

### Full Packet Capture
**Methods:**  

- Network TAP  
- Port Mirroring (SPAN)  

**Tools:**  
- Wireshark  
- tcpdump  
- Snort  
- Suricata  
- Zeek  

---

###  Network Statistics
**Protocols:**  
- NetFlow  
- IPFIX  

**Used to detect:** C2 traffic, data exfiltration, lateral movement  

---

##  Practical Exercise

### Scenario 1 – Malicious PowerShell Download
Captured HTTP response:
![Uploading Screenshot 2026-02-21 215546.png…]()

![Uploading Screenshot 2026-02-21 215627.png…]()

![Uploading Screenshot 2026-02-21 220011.png…]()

<img width="545" height="49" alt="Screenshot 2026-02-21 215937" src="https://github.com/user-attachments/assets/fa2aa397-ac06-4d44-b10b-dd7772af1dbd" />

Content-Disposition: attachment; filename="install.ps1"
Body Preview:
THM{FoundTheMalware}


**Flag:**  THM{FoundTheMalware}  

---

###  Scenario 2 – DNS C2 Infiltration
Captured DNS TXT record:
<img width="1354" height="627" alt="Screenshot 2026-02-21 220113" src="https://github.com/user-attachments/assets/1f329684-719f-40b1-ba31-e2b6788f161a" />

<img width="1353" height="626" alt="Screenshot 2026-02-21 220145" src="https://github.com/user-attachments/assets/eefbc038-baf6-40b7-95c5-eb723f9e3cf7" />

<img width="545" height="73" alt="Screenshot 2026-02-21 220221" src="https://github.com/user-attachments/assets/d497e4f4-681b-47d3-b7dd-953575e538e2" />

![Uploading Screenshot 2026-02-21 220241.png…]()

data: THM{C2CommandFound}


**Flag:**  THM{C2CommandFound}  

---

## Task 6 – Conclusion
In this room, we learned:

- What Network Traffic Analysis is  
- Why it is critical for SOC analysts  
- How attackers use DNS tunneling  
- How session hijacking is detected  
- How fragmentation evades IDS  
- Difference between North-South & East-West traffic  
- How to capture traffic using TAP and SPAN  
- How to extract malicious indicators from packet captures  

This room builds the foundation for deeper packet analysis using **Wireshark** in the next module.

<img width="1354" height="629" alt="Screenshot 2026-02-21 224902" src="https://github.com/user-attachments/assets/89f32a2c-7cb1-474f-9b64-200c423d9f31" />

