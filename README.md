
# Fast Port Scanner Script Documentation

## Overview
This script is a multi-threaded port scanner designed to quickly identify open ports on a target host within a specified range. It leverages Python's socket module for network connections, threading for concurrent scanning, and argparse for command-line argument parsing. Additionally, it includes a function for basic OS detection on the target using an SSH command.

## Dependencies
- **argparse**: Parses command-line arguments.
- **socket**: Establishes TCP connections to check port status.
- **colorama**: Provides colored output for different states (open/closed ports).
- **threading** and **queue**: Manages multi-threaded execution and work queues.
- **subprocess**: Executes shell commands to obtain system information from the target.
- **sys**: Handles system-level operations, such as terminating the script.

## Global Constants
- **N_THREADS**: Number of threads for concurrent scanning (set to 200 by default).
- **maximal_ports**: Upper limit for the number of ports (default 1025).
- **Colors (GREEN, GRAY, RESET)**: Used to color-code output for better readability.

## Functions

### `port_scan(port)`
- **Parameters**: `port` - The port number to scan.
- **Description**: Attempts to connect to the specified port on the target host. If successful, it indicates that the port is open; otherwise, it prints the port as closed.
- **Locking Mechanism**: Uses `print_lock` to ensure thread-safe output to the console.

### `get_os(host)`
- **Parameters**: `host` - The IP or hostname of the target.
- **Description**: Attempts to retrieve OS information of the target via SSH. Runs the `uname -a` command on the remote machine. Note that the `UNAME@HOST` placeholder should be replaced with actual credentials for this function to work.
- **Output**: Prints the OS information if the connection is successful.

### `scan_thread()`
- **Description**: Continuously pulls port numbers from the queue and calls `port_scan()` to scan each port. Once a port scan is complete, it marks the task as done in the queue.

### `main(host, ports)`
- **Parameters**:
  - `host` - The target IP or hostname.
  - `ports` - List of port numbers to scan.
- **Description**: Initializes and starts the threads for port scanning, enqueues each port in the range for scanning, and waits for all threads to complete their tasks.

## Usage
The script takes the following command-line arguments:
- **host** (required) - The IP address or hostname to scan.
- **--ports / -p** (optional) - Specifies the port range in the format start-end (default is 1-65535).

### Example Command
```bash
python fast_port_scaner.py 192.168.1.1 -p 1-1024
```
This command scans the first 1024 ports on the host `192.168.1.1`.

## Execution Flow
1. The script parses command-line arguments to retrieve the target host and port range.
2. It splits the port range into `start_port` and `end_port` and generates a list of ports to scan.
3. The `main` function is called with the host and list of ports, which:
   - Initializes threads and assigns each thread to `scan_thread()`.
   - Enqueues ports for scanning and waits for all threads to finish.
4. Each thread scans ports in parallel, improving scan speed on larger port ranges.

## Notes and Warnings
- **SSH Connection in get_os()**: This function is intended for retrieving OS information over SSH. It currently uses placeholder credentials (`UNAME@HOST`). Replace these placeholders with real credentials for the function to work.
- **Thread Safety**: The script uses a lock (`print_lock`) to prevent simultaneous console output from multiple threads.
- **Permissions**: Ensure you have permission to scan the target host, as unauthorized scanning may be illegal and against network policies.
