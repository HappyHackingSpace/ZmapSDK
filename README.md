# ZMap SDK

Python SDK for the ZMap network scanner with REST API support.

## Installation

```bash
pip install zmapsdk
```

## SDK Usage

```python
from zmapsdk import ZMap

# Initialize ZMap SDK
zmap = ZMap()

# Perform a scan
results = zmap.scan(target_port=80, bandwidth="10M")
print(f"Found {len(results)} open hosts")

# Create a blocklist
zmap.create_blocklist_file(["192.168.0.0/16", "10.0.0.0/8"], "private_ranges.txt")

# Generate a standard blocklist
zmap.generate_standard_blocklist("standard_blocklist.txt")
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

## License

MIT
