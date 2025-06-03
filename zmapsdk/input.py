"""
Input handling module for ZMap SDK
"""

import ipaddress
import os
from typing import Any

from zmapsdk.exceptions import ZMapInputError


class ZMapInput:
    """
    Class for handling ZMap input options like target lists, blocklists, and allowlists
    """

    def __init__(self):
        """Initialize the input handler"""
        self.blocklist_file: str | None = None
        self.allowlist_file: str | None = None
        self.input_file: str | None = None
        self.target_subnets: list[str] = []
        self.ignore_blocklist: bool = False
        self.ignore_invalid_hosts: bool = False

    def add_subnet(self, subnet: str) -> None:
        """
        Add a subnet to the target list

        Args:
            subnet: Subnet in CIDR notation (e.g., '192.168.0.0/16')

        Raises:
            ZMapInputError: If the subnet is invalid
        """
        try:
            ipaddress.ip_network(subnet)
            self.target_subnets.append(subnet)
        except ValueError as e:
            raise ZMapInputError(f"Invalid subnet: {subnet} - {e!s}")

    def add_subnets(self, subnets: list[str]) -> None:
        """
        Add multiple subnets to the target list

        Args:
            subnets: List of subnets in CIDR notation

        Raises:
            ZMapInputError: If any subnet is invalid
        """
        for subnet in subnets:
            self.add_subnet(subnet)

    def set_blocklist_file(self, file_path: str) -> None:
        """
        Set the blocklist file

        Args:
            file_path: Path to the blocklist file

        Raises:
            ZMapInputError: If the file doesn't exist or isn't readable
        """
        if not os.path.isfile(file_path):
            raise ZMapInputError(f"Blocklist file not found: {file_path}")
        if not os.access(file_path, os.R_OK):
            raise ZMapInputError(f"Blocklist file not readable: {file_path}")
        self.blocklist_file = file_path

    def set_allowlist_file(self, file_path: str) -> None:
        """
        Set the allowlist file

        Args:
            file_path: Path to the allowlist file

        Raises:
            ZMapInputError: If the file doesn't exist or isn't readable
        """
        if not os.path.isfile(file_path):
            raise ZMapInputError(f"Allowlist file not found: {file_path}")
        if not os.access(file_path, os.R_OK):
            raise ZMapInputError(f"Allowlist file not readable: {file_path}")
        self.allowlist_file = file_path

    def set_input_file(self, file_path: str) -> None:
        """
        Set the input file for targets

        Args:
            file_path: Path to the input file

        Raises:
            ZMapInputError: If the file doesn't exist or isn't readable
        """
        if not os.path.isfile(file_path):
            raise ZMapInputError(f"Input file not found: {file_path}")
        if not os.access(file_path, os.R_OK):
            raise ZMapInputError(f"Input file not readable: {file_path}")
        self.input_file = file_path

    def create_blocklist_file(self, subnets: list[str], output_file: str) -> str:
        """
        Create a blocklist file from a list of subnets

        Args:
            subnets: List of subnet CIDRs to blocklist
            output_file: Path to save the blocklist file

        Returns:
            Path to the created blocklist file

        Raises:
            ZMapInputError: If a subnet is invalid or file can't be created
        """
        # Validate subnets
        for subnet in subnets:
            try:
                ipaddress.ip_network(subnet)
            except ValueError as e:
                raise ZMapInputError(f"Invalid subnet in blocklist: {subnet} - {e!s}")

        # Write to file
        try:
            with open(output_file, "w") as f:
                f.write("\n".join(subnets))
        except OSError as e:
            raise ZMapInputError(f"Failed to create blocklist file: {e!s}")

        self.blocklist_file = output_file
        return output_file

    def create_allowlist_file(self, subnets: list[str], output_file: str) -> str:
        """
        Create a allowlist file from a list of subnets

        Args:
            subnets: List of subnet CIDRs to allowlist
            output_file: Path to save the allowlist file

        Returns:
            Path to the created allowlist file

        Raises:
            ZMapInputError: If a subnet is invalid or file can't be created
        """
        # Validate subnets
        for subnet in subnets:
            try:
                ipaddress.ip_network(subnet)
            except ValueError as e:
                raise ZMapInputError(f"Invalid subnet in allowlist: {subnet} - {e!s}")

        # Write to file
        try:
            with open(output_file, "w") as f:
                f.write("\n".join(subnets))
        except OSError as e:
            raise ZMapInputError(f"Failed to create allowlist file: {e!s}")

        self.allowlist_file = output_file
        return output_file

    def create_target_file(self, targets: list[str], output_file: str) -> str:
        """
        Create an input file for specific target IPs

        Args:
            targets: List of IP addresses to scan
            output_file: Path to save the input file

        Returns:
            Path to the created input file

        Raises:
            ZMapInputError: If an IP is invalid or file can't be created
        """
        # Validate IPs
        for ip in targets:
            try:
                ipaddress.ip_address(ip)
            except ValueError as e:
                raise ZMapInputError(f"Invalid IP address: {ip} - {e!s}")

        # Write to file
        try:
            with open(output_file, "w") as f:
                f.write("\n".join(targets))
        except OSError as e:
            raise ZMapInputError(f"Failed to create target file: {e!s}")

        self.input_file = output_file
        return output_file

    def generate_standard_blocklist(self, output_file: str) -> str:
        """
        Generate a blocklist file with standard private network ranges

        Args:
            output_file: Path to save the blocklist file

        Returns:
            Path to the created blocklist file
        """
        private_ranges = [
            "10.0.0.0/8",  # RFC1918 private network
            "172.16.0.0/12",  # RFC1918 private network
            "192.168.0.0/16",  # RFC1918 private network
            "127.0.0.0/8",  # Loopback
            "169.254.0.0/16",  # Link-local
            "224.0.0.0/4",  # Multicast
            "240.0.0.0/4",  # Reserved
            "192.0.2.0/24",  # TEST-NET for documentation
            "198.51.100.0/24",  # TEST-NET-2 for documentation
            "203.0.113.0/24",  # TEST-NET-3 for documentation
        ]

        return self.create_blocklist_file(private_ranges, output_file)

    def to_dict(self) -> dict[str, Any]:
        """Convert input configuration to a dictionary for command-line options"""
        result = {}

        if self.blocklist_file:
            result["blocklist_file"] = self.blocklist_file

        if self.allowlist_file:
            result["allowlist_file"] = self.allowlist_file

        if self.input_file:
            result["input_file"] = self.input_file

        if self.ignore_blocklist:
            result["ignore_blocklist"] = True

        if self.ignore_invalid_hosts:
            result["ignore_invalid_hosts"] = True

        if self.target_subnets:
            result["subnets"] = self.target_subnets

        return result
