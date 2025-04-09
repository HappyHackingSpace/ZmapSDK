# ZMap SDK

A Python SDK for the ZMap network scanner that provides an easy-to-use interface for network scanning operations.

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
```

## Core Components

The ZMap SDK consists of several core components:

- **ZMap**: The main class that provides the interface to ZMap
- **ZMapScanConfig**: Handles scan configuration parameters
- **ZMapInput**: Manages input sources (subnets, whitelists, blacklists)
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

### Using Blacklists and Whitelists

```python
from zmapsdk import ZMap

zmap = ZMap()

# Using a blacklist file
zmap.blacklist_from_file("/path/to/blacklist.txt")

# Creating a blacklist file
zmap.create_blacklist_file(
    subnets=["10.0.0.0/8", "192.168.0.0/16"],
    output_file="private_ranges.conf"
)

# Using a whitelist file
zmap.whitelist_from_file("/path/to/whitelist.txt")

# Run scan with blacklist
results = zmap.scan(
    target_port=443,
    blacklist_file="private_ranges.conf"
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
- `blacklist_from_file(blacklist_file)`: Validate and use a blacklist file
- `whitelist_from_file(whitelist_file)`: Validate and use a whitelist file
- `create_blacklist_file(subnets, output_file)`: Create a blacklist file
- `create_whitelist_file(subnets, output_file)`: Create a whitelist file
- `create_target_file(targets, output_file)`: Create a file with target IPs
- `generate_standard_blacklist(output_file)`: Generate standard blacklist
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
  - `ignore_invalid_hosts`: Ignore invalid hosts in whitelist/blacklist file
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

This project is licensed under the MIT License - see the LICENSE file for details.
