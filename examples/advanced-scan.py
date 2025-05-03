from zmapsdk import ZMap, ZMapScanConfig

# Initialize ZMap with more advanced configuration
config = ZMapScanConfig(
    target_port=80,
    bandwidth="10M",  # Set bandwidth limit to 10 Mbps
    rate=1000,  # Limit to 1000 packets per second
    cooldown_time=5,  # Wait 5 seconds between scan attempts
    retries=2,  # Retry failed connections twice
)

zmap = ZMap()
zmap.config = config

# Run scan with multiple subnets and custom output
result = zmap.scan(
    subnets=[
        "192.168.1.0/24",
        "192.168.2.0/24",
    ],
    output_file="scan_results.csv",
    output_fields=["saddr", "daddr", "sport", "dport", "seqnum", "timestamp"],
)

# Print detailed results
print(f"Scan completed. Found {len(result)} results:")
for ip in result:
    print(f"Open port 80 at: {ip}")
