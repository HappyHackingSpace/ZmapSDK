# ZMap SDK

A Python SDK for the ZMap network scanner that provides an easy-to-use interface for network scanning operations with REST API support.

## Installation

### Prerequisites

- Python 3.6 or higher
- ZMap installed on your system - [ZMap Installation Guide](https://github.com/zmap/zmap/blob/main/INSTALL.md)

### Installing the SDK

```bash
pip install zmapsdk
```

Or install from source:

```bash
git clone https://github.com/HappyHackingSpace/ZmapSDK
cd zmapsdk
pip install .
```

## Quick Start

```python
from zmapsdk import ZMap

# Initialize the ZMap SDK
zmap = ZMap()  # Uses 'zmap' from PATH by default

# Run a basic scan on port 80
results = zmap.scan(
    target_port=80,
    subnets=["192.168.1.0/24"],  # Scan your local network
    bandwidth="1M"  # Limit bandwidth to 1 Mbps
)

# Print the results
print(f"Found {len(results)} open ports")
for ip in results:
    print(f"Open port at: {ip}")

# Create a blocklist
zmap.create_blocklist_file(["192.168.0.0/16", "10.0.0.0/8"], "private_ranges.txt")

# Generate a standard blocklist
zmap.generate_standard_blocklist("standard_blocklist.txt")
```

## Core Components

The ZMap SDK consists of several core components:

- **ZMap**: The main class that provides the interface to ZMap
- **ZMapScanConfig**: Handles scan configuration parameters
- **ZMapInput**: Manages input sources (subnets, allowlists, blocklists)
- **ZMapOutput**: Controls output formatting and destinations
- **ZMapRunner**: Executes ZMap commands and captures results
- **ZMapParser**: Parses ZMap output into structured data

## Basic Usage

### Specifying a Custom ZMap Path

```python
from zmapsdk import ZMap

# Initialize with custom path to the ZMap executable
zmap = ZMap(zmap_path="/usr/local/bin/zmap")

# Run scan as usual
results = zmap.scan(target_port=80, subnets=["192.168.0.0/24"])
```

### Scanning a Specific Port

```python
from zmapsdk import ZMap

zmap = ZMap()
results = zmap.scan(target_port=443, subnets=["10.0.0.0/8"])
```

### Configuring Bandwidth and Rate

```python
from zmapsdk import ZMap, ZMapScanConfig

# Option 1: Configure via parameters
results = zmap.scan(
    target_port=22,
    bandwidth="10M",  # 10 Mbps
    subnets=["192.168.0.0/16"]
)

# Option 2: Configure via config object
config = ZMapScanConfig(
    target_port=22,
    bandwidth="10M"
)
zmap = ZMap()
zmap.config = config
results = zmap.scan(subnets=["192.168.0.0/16"])
```

### Specifying Output File

```python
from zmapsdk import ZMap

zmap = ZMap()
results = zmap.scan(
    target_port=80,
    subnets=["172.16.0.0/12"],
    output_file="scan_results.csv"
)
```

### Using Blocklists and Allowlists

```python
from zmapsdk import ZMap

zmap = ZMap()

# Using a blocklist file
zmap.blocklist_from_file("/path/to/blocklist.txt")

# Creating a blocklist file
zmap.create_blocklist_file(
    subnets=["10.0.0.0/8", "192.168.0.0/16"],
    output_file="private_ranges.conf"
)

# Using a allowlist file
zmap.allowlist_from_file("/path/to/allowlist.txt")

# Run scan with blocklist
results = zmap.scan(
    target_port=443,
    blocklist_file="private_ranges.conf"
)
```

### Controlling Scan Behavior

```python
from zmapsdk import ZMap

zmap = ZMap()
results = zmap.scan(
    target_port=80,
    max_targets=1000,      # Limit to 1000 targets
    max_runtime=60,        # Run for max 60 seconds
    cooldown_time=5,       # Wait 5 seconds after sending last probe
    probes=3,              # Send 3 probes to each IP
    dryrun=True            # Don't actually send packets (test mode)
)
```

### Advanced Configuration

```python
from zmapsdk import ZMap, ZMapScanConfig

# Create configuration
config = ZMapScanConfig(
    target_port=443,
    bandwidth="100M",
    interface="eth0",
    source_ip="192.168.1.5",
    source_port="40000-50000",  # Random source port in range
    max_targets="10%",          # Scan 10% of address space
    sender_threads=4,           # Use 4 threads for sending
    notes="HTTPS scanner for internal audit",
    seed=123456                 # Set random seed for reproducibility
)

# Initialize ZMap with configuration
zmap = ZMap()
zmap.config = config

# Run scan
results = zmap.scan(subnets=["10.0.0.0/16"])
```

## Processing Results

### Parsing Results

```python
from zmapsdk import ZMap

zmap = ZMap()

# Run scan and save results
zmap.scan(
    target_port=22,
    subnets=["192.168.1.0/24"],
    output_file="scan_results.csv",
    output_fields=["saddr", "daddr", "sport", "dport", "classification"]
)

# Parse the results file
parsed_results = zmap.parse_results("scan_results.csv")

# Process the structured data
for result in parsed_results:
    print(f"Source IP: {result['saddr']}, Classification: {result['classification']}")

# Extract just the IPs
ip_list = zmap.extract_ips(parsed_results)
```

### Working with Large Result Sets

```python
from zmapsdk import ZMap

zmap = ZMap()

# For large scans, stream the results instead of loading all at once
for result in zmap.stream_results("large_scan_results.csv"):
    process_result(result)  # Your processing function

# Count results without loading everything
count = zmap.count_results("large_scan_results.csv")
print(f"Found {count} results")
```

## REST API

ZMap SDK includes a REST API that allows you to control ZMap operations remotely.

### Starting the API Server

You can start the API server in two ways:

#### From Command Line

```bash
# Start API server on default host (127.0.0.1) and port (8000)
zmapsdk api

# Start API server with custom host and port
zmapsdk api --host 0.0.0.0 --port 9000

# Start API server with verbose logging
zmapsdk api -v
```

#### From Python

```python
from zmapsdk import APIServer

# Create and start the API server
server = APIServer(host="0.0.0.0", port=8000)
server.run()
```

### API Endpoints

The REST API provides the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Basic information about the API |
| `/probe-modules` | GET | List available probe modules |
| `/output-modules` | GET | List available output modules |
| `/output-fields` | GET | List available output fields for a probe module |
| `/interfaces` | GET | List available network interfaces |
| `/scan-sync` | POST | Run a scan synchronously and return results |
| `/blocklist` | POST | Create a blocklist file from a list of subnets |
| `/standard-blocklist` | POST | Generate a standard blocklist file |
| `/allowlist` | POST | Create an allowlist file from a list of subnets |

### API Documentation

The API includes automatic documentation using Swagger UI and ReDoc:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example API Requests

#### Basic Information

```bash
curl -X GET "http://localhost:8000/"
```

Response:
```json
{
  "name": "ZMap SDK API",
  "version": "2.1.1",
  "description": "REST API for ZMap network scanner"
}
```

#### List Available Probe Modules

```bash
curl -X GET "http://localhost:8000/probe-modules"
```

Response:
```json
["tcp_synscan", "icmp_echoscan", "udp", "module_ntp", "module_dns"]
```

#### List Available Output Modules

```bash
curl -X GET "http://localhost:8000/output-modules"
```

Response:
```json
["csv", "json", "extended_file", "redis"]
```

#### List Available Network Interfaces

```bash
curl -X GET "http://localhost:8000/interfaces"
```

Response:
```json
["eth0", "lo", "wlan0"]
```

#### Run a Scan

```bash
curl -X POST "http://localhost:8000/scan-sync" \
  -H "Content-Type: application/json" \
  -d '{
    "target_port": 80,
    "bandwidth": "10M",
    "probe_module": "tcp_synscan",
    "return_results": true
  }'
```

Response:
```json
{
  "scan_id": "direct_scan",
  "status": "completed",
  "ips_found": ["192.168.1.1", "192.168.1.2", "10.0.0.1"]
}
```

#### Create a Blocklist

```bash
curl -X POST "http://localhost:8000/blocklist" \
  -H "Content-Type: application/json" \
  -d '{
    "subnets": ["192.168.0.0/16", "10.0.0.0/8"]
  }'
```

Response:
```json
{
  "file_path": "/tmp/zmap_blocklist_a1b2c3.txt",
  "message": "Blocklist file created with 2 subnets"
}
```

#### Generate a Standard Blocklist

```bash
curl -X POST "http://localhost:8000/standard-blocklist" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "file_path": "/tmp/zmap_std_blocklist_x1y2z3.txt",
  "message": "Standard blocklist file created"
}
```

#### Create an Allowlist

```bash
curl -X POST "http://localhost:8000/allowlist" \
  -H "Content-Type: application/json" \
  -d '{
    "subnets": ["1.2.3.0/24", "5.6.7.0/24"],
    "output_file": "my_allowlist.txt"
  }'
```

Response:
```json
{
  "file_path": "my_allowlist.txt",
  "message": "Allowlist file created with 2 subnets"
}
```

## API Reference

### ZMap Class

The main interface for the ZMap SDK.

#### Methods

- `scan(target_port, subnets, output_file, **kwargs)`: Perform a scan and return the results
- `run(**kwargs)`: Run ZMap with specified parameters
- `get_probe_modules()`: Get list of available probe modules
- `get_output_modules()`: Get list of available output modules
- `get_output_fields(probe_module)`: Get list of available output fields
- `get_interfaces()`: Get list of available network interfaces
- `get_version()`: Get ZMap version
- `blocklist_from_file(blocklist_file)`: Validate and use a blocklist file
- `allowlist_from_file(allowlist_file)`: Validate and use a allowlist file
- `create_blocklist_file(subnets, output_file)`: Create a blocklist file
- `create_allowlist_file(subnets, output_file)`: Create a allowlist file
- `create_target_file(targets, output_file)`: Create a file with target IPs
- `generate_standard_blocklist(output_file)`: Generate standard blocklist
- `parse_results(file_path, fields)`: Parse scan results into structured data
- `parse_metadata(file_path)`: Parse scan metadata
- `extract_ips(results, ip_field)`: Extract IPs from results
- `stream_results(file_path, fields)`: Stream results from a file
- `count_results(file_path)`: Count results in a file

### ZMapScanConfig Class

Handles configuration for ZMap scans.

#### Fields

- **Core Options**:
  - `target_port`: Port number to scan
  - `bandwidth`: Send rate in bits/second (supports G, M, K suffixes)
  - `rate`: Send rate in packets/sec
  - `cooldown_time`: How long to continue receiving after sending last probe
  - `interface`: Network interface to use
  - `source_ip`: Source address for scan packets
  - `source_port`: Source port(s) for scan packets
  - `gateway_mac`: Gateway MAC address
  - `source_mac`: Source MAC address
  - `target_mac`: Target MAC address
  - `vpn`: Send IP packets instead of Ethernet (for VPNs)

- **Scan Control Options**:
  - `max_targets`: Cap number of targets to probe
  - `max_runtime`: Cap length of time for sending packets
  - `max_results`: Cap number of results to return
  - `probes`: Number of probes to send to each IP
  - `retries`: Max number of times to try to send packet if send fails
  - `dryrun`: Don't actually send packets
  - `seed`: Seed used to select address permutation
  - `shards`: Total number of shards
  - `shard`: Which shard this scan is (0 indexed)

- **Advanced Options**:
  - `sender_threads`: Threads used to send packets
  - `cores`: Comma-separated list of cores to pin to
  - `ignore_invalid_hosts`: Ignore invalid hosts in allowlist/blocklist file
  - `max_sendto_failures`: Maximum NIC sendto failures before scan is aborted
  - `min_hitrate`: Minimum hitrate that scan can hit before scan is aborted

- **Metadata Options**:
  - `notes`: User-specified notes for scan metadata
  - `user_metadata`: User-specified JSON metadata

## Examples

Check out the `examples/` directory for practical examples:

- `basic-scan.py` - Simple port scanning example showing essential ZMap SDK usage
- `advanced-scan.py` - Advanced scanning example with custom configurations and output processing

## Requirements

- Python 3.6+
- ZMap network scanner installed on the system

## Contributing

Contributions to the ZMap SDK are welcome! Here's how you can contribute:

1. **Report Issues**: Report bugs or suggest features by opening an issue on the GitHub repository.

2. **Submit Pull Requests**: Implement new features or fix bugs and submit a pull request.

3. **Improve Documentation**: Help improve the documentation or add more examples.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/HappyHackingSpace/ZmapSDK.git
cd ZmapSDK

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Coding Standards

- Follow PEP 8 style guidelines
- Write unit tests for new features
- Update documentation to reflect changes

## Disclaimer

The ZMapSDK is provided for legitimate network research and security assessments only. Please use this tool responsibly and ethically.

**Important considerations:**

- Always ensure you have proper authorization before scanning any network or system.
- Comply with all applicable laws and regulations regarding network scanning in your jurisdiction.
- Be aware that network scanning may be interpreted as malicious activity by network administrators and may trigger security alerts.
- The authors and contributors of this SDK are not responsible for any misuse or damage caused by this software.
- Network scanning may cause disruption to services or systems; use appropriate bandwidth and rate limiting settings.

Before using this SDK for any network scanning operation, especially on production networks, consult with network administrators and obtain proper written permission.

## License

MIT
