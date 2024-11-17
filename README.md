
# **NetworkScanner Documentation**

## **Overview**
The `NetworkScanner` script is a Python-based command-line tool for scanning networks and identifying open ports on hosts. It supports scanning based on specific network interfaces, custom IP ranges, and configurable port ranges. The results are saved to a JSON file for analysis.

---

## **Installation and Requirements**
### **Prerequisites**
Ensure the following are installed:
- **Python**: Version 3.8 or later.
- **Required Libraries**: Install the dependencies using the command:
  ```bash
  pip install netifaces
  ```

### **Optional Tools**
- The `lsof` command-line utility is recommended for identifying services on open ports.

---

## **Usage**
Run the script with appropriate command-line arguments to customize the scanning process. 

### **Command-line Arguments**
| Argument          | Description                                                                                          | Example                          |
|-------------------|------------------------------------------------------------------------------------------------------|----------------------------------|
| `-i`, `--interface` | Specify the network interface to scan. Only hosts on the network of this interface will be scanned. | `--interface eno1`              |
| `-r`, `--ip-range`  | Provide a custom IP range in CIDR notation to scan. Overrides the interface option if provided.     | `--ip-range 192.168.1.0/24`     |
| `-p`, `--port-range`| Define a range of ports to scan, formatted as `start-end`. If not specified, all ports are scanned. | `--port-range 20-80`            |

### **How to Run**
#### 1. Scan a specific network interface:
```bash
python scanner.py --interface eno1
```

#### 2. Scan a custom IP range:
```bash
python scanner.py --ip-range 192.168.1.0/24
```

#### 3. Scan specific ports:
```bash
python scanner.py --port-range 20-80
```

#### 4. Combine options:
```bash
python scanner.py --interface eno1 --port-range 22-1024
```

---

## **Output**
### **Files Generated**
1. **`open_ports.json`**:
   Contains all scanned hosts and their open ports in JSON format.
   ```json
   {
       "192.168.1.1": [22, 80, 443],
       "192.168.1.2": [22, 8080]
   }
   ```

2. **Console Output**:
   Displays progress and details of open ports during the scan:
   ```
   Port 22 is open for host 192.168.1.1
   Port 80 is open for host 192.168.1.1
   ```

---

## **Internal Functions**
### **1. `get_all_local_ips()`**
   - Retrieves all local IP addresses associated with active network interfaces.
   - **Returns**: A dictionary mapping interfaces to their IP addresses.

### **2. `get_net_interface(interface)`**
   - Finds the IP address of a specified network interface.
   - **Input**: `interface` (e.g., `eno1`).
   - **Returns**: The IP address of the interface or `None` if not found.

### **3. `get_custom_hosts(ip_range)`**
   - Generates a list of host IPs from a provided CIDR range.
   - **Input**: `ip_range` (e.g., `192.168.1.0/24`).
   - **Returns**: A list of host IPs.

### **4. `port_scan(host, ports)`**
   - Performs a scan on the given ports for a single host.
   - **Inputs**:
     - `host`: Target host IP address.
     - `ports`: List or range of ports to scan.
   - **Returns**: A list of open ports.

### **5. `identify_service(port)`**
   - Uses the `lsof` utility to identify the service running on a port.
   - **Input**: `port` (e.g., `80`).
   - **Returns**: Service name or `Unknown` if not detected.

---

## **Error Handling**
- **Invalid Network Interface**: If the specified network interface is invalid or has no IP, an error message is shown.
- **Invalid IP Range**: The script validates the provided IP range. If invalid, it exits with an error.
- **Invalid Port Range**: An incorrectly formatted port range triggers a descriptive error message.

---

## **Example Workflow**
### **Scenario**: Scan a network for open SSH (22) and HTTP (80) ports.
1. Identify the active network interface using `ifconfig` or `ip a`.
2. Run the script:
   ```bash
   python scanner.py --interface eno1 --port-range 22-80
   ```
3. View results in `open_ports.json`:
   ```json
   {
       "192.168.1.1": [22, 80],
       "192.168.1.2": [22]
   }
   ```

---

## **Limitations**
1. **Asynchronous Scanning**:
   - Uses non-blocking sockets for efficiency but may skip some ports if the host is heavily loaded.
2. **Service Identification**:
   - Relies on `lsof`, which may not always detect services due to permission restrictions.

---

## **Extending the Script**
To extend the script, consider:
1. Adding support for scanning multiple IP ranges.
2. Including an option to exclude certain hosts or ports.
3. Improving service detection by using `nmap` or similar tools.

---

## ⚠️ Warning

This code is intended **only for ethical purposes** such as network diagnostics, security testing on networks you own, or networks where you have explicit permission from the owner. 

**Unauthorized use of this code to scan networks without proper consent is illegal and unethical.** Misuse may result in severe legal consequences, including fines or imprisonment, depending on your jurisdiction.

Always ensure compliance with local laws and regulations before running this script. The authors and contributors to this script are not responsible for any misuse or harm caused by its improper application.
