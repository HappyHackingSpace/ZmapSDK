"""
Configuration module for ZMap SDK
"""

import json
from dataclasses import asdict, dataclass
from typing import Any

from .exceptions import ZMapConfigError


@dataclass
class ZMapScanConfig:
    """
    Configuration for a ZMap scan

    Args:
        target_port: Port number to scan (for TCP and UDP scans)
        bandwidth: Set send rate in bits/second (supports suffixes G, M and K)
        rate: Set send rate in packets/sec
        cooldown_time: How long to continue receiving after sending last probe
        interface: Specify network interface to use
        source_ip: Source address(es) for scan packets
        source_port: Source port(s) for scan packets
        gateway_mac: Specify gateway MAC address
        source_mac: Source MAC address
        target_mac: Target MAC address (when ARP is disabled)
        vpn: Sends IP packets instead of Ethernet (for VPNs)
        max_targets: Cap number of targets to probe
        max_runtime: Cap length of time for sending packets
        max_results: Cap number of results to return
        probes: Number of probes to send to each IP
        retries: Max number of times to try to send packet if send fails
        dryrun: Don't actually send packets
        seed: Seed used to select address permutation
        shards: Set the total number of shards
        shard: Set which shard this scan is (0 indexed)
        sender_threads: Threads used to send packets
        cores: Comma-separated list of cores to pin to
        ignore_invalid_hosts: Ignore invalid hosts in allowlist/blocklist file
        max_sendto_failures: Maximum NIC sendto failures before scan is aborted
        min_hitrate: Minimum hitrate that scan can hit before scan is aborted
        notes: Inject user-specified notes into scan metadata
        user_metadata: Inject user-specified JSON metadata into scan metadata
    """

    # Core Options
    target_port: int | None = None
    bandwidth: str | None = None
    rate: int | None = None
    cooldown_time: int | None = None
    interface: str | None = None
    source_ip: str | None = None
    source_port: int | str | None = None
    gateway_mac: str | None = None
    source_mac: str | None = None
    target_mac: str | None = None
    vpn: bool = False

    # Scan Control Options
    max_targets: int | str | None = None
    max_runtime: int | None = None
    max_results: int | None = None
    probes: int | None = None
    retries: int | None = None
    dryrun: bool = False
    seed: int | None = None
    shards: int | None = None
    shard: int | None = None

    # Advanced Options
    sender_threads: int | None = None
    cores: list[int] | str | None = None
    ignore_invalid_hosts: bool = False
    max_sendto_failures: int | None = None
    min_hitrate: float | None = None

    # Metadata Options
    notes: str | None = None
    user_metadata: dict[str, Any] | str | None = None

    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate()

    def _validate(self) -> None:
        """Validate the configuration"""
        if self.target_port is not None and not (0 <= self.target_port <= 65535):
            raise ZMapConfigError(
                f"Invalid target port: {self.target_port}. Must be between 0 and 65535.",
            )

        if self.rate is not None and self.bandwidth is not None:
            raise ZMapConfigError("Cannot specify both rate and bandwidth.")

        if self.source_port is not None:
            if isinstance(self.source_port, str) and "-" in self.source_port:
                parts = self.source_port.split("-")
                if len(parts) != 2 or not all(p.isdigit() for p in parts):
                    raise ZMapConfigError(
                        f"Invalid source port range: {self.source_port}.",
                    )
                start, end = map(int, parts)
                if not (0 <= start <= end <= 65535):
                    raise ZMapConfigError(
                        f"Invalid source port range: {self.source_port}. Must be between 0 and 65535.",
                    )
            elif isinstance(self.source_port, int) and not (
                0 <= self.source_port <= 65535
            ):
                raise ZMapConfigError(
                    f"Invalid source port: {self.source_port}. Must be between 0 and 65535.",
                )

        if self.max_targets is not None and isinstance(self.max_targets, str):
            if not self.max_targets.endswith("%"):
                try:
                    int(self.max_targets)
                except ValueError:
                    raise ZMapConfigError(
                        f"Invalid max_targets: {self.max_targets}. Must be an integer or percentage.",
                    )

        # Validate MAC addresses
        for mac_field in ["gateway_mac", "source_mac", "target_mac"]:
            mac = getattr(self, mac_field)
            if mac is not None and not self._is_valid_mac(mac):
                raise ZMapConfigError(
                    f"Invalid {mac_field}: {mac}. Must be in format 'XX:XX:XX:XX:XX:XX'.",
                )

    @staticmethod
    def _is_valid_mac(mac: str) -> bool:
        """Check if a string is a valid MAC address"""
        import re

        return bool(re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac))

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to a dictionary, removing None values"""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result

    def to_json(self) -> str:
        """Convert configuration to a JSON string"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ZMapScanConfig":
        """Create a configuration from a dictionary"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "ZMapScanConfig":
        """Create a configuration from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def save_to_file(self, filename: str) -> None:
        """Save configuration to a file as JSON"""
        with open(filename, "w") as f:
            f.write(self.to_json())

    @classmethod
    def load_from_file(cls, filename: str) -> "ZMapScanConfig":
        """Load configuration from a JSON file"""
        with open(filename) as f:
            return cls.from_json(f.read())
