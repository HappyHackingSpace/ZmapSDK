"""
Input handling module for ZMap SDK
"""

import os
import ipaddress
from typing import List, Optional, Set, Union, Dict, Any

from .exceptions import ZMapInputError


class ZMapInput:
    """
    Class for handling ZMap input options like target lists, blacklists, and whitelists
    """
    
    def __init__(self):
        """Initialize the input handler"""
        self.blacklist_file: Optional[str] = None
        self.whitelist_file: Optional[str] = None
        self.input_file: Optional[str] = None
        self.target_subnets: List[str] = []
        self.ignore_blacklist: bool = False
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
            raise ZMapInputError(f"Invalid subnet: {subnet} - {str(e)}")
    
    def add_subnets(self, subnets: List[str]) -> None:
        """
        Add multiple subnets to the target list
        
        Args:
            subnets: List of subnets in CIDR notation
            
        Raises:
            ZMapInputError: If any subnet is invalid
        """
        for subnet in subnets:
            self.add_subnet(subnet)
    
    def set_blacklist_file(self, file_path: str) -> None:
        """
        Set the blacklist file
        
        Args:
            file_path: Path to the blacklist file
            
        Raises:
            ZMapInputError: If the file doesn't exist or isn't readable
        """
        if not os.path.isfile(file_path):
            raise ZMapInputError(f"Blacklist file not found: {file_path}")
        if not os.access(file_path, os.R_OK):
            raise ZMapInputError(f"Blacklist file not readable: {file_path}")
        self.blacklist_file = file_path
    
    def set_whitelist_file(self, file_path: str) -> None:
        """
        Set the whitelist file
        
        Args:
            file_path: Path to the whitelist file
            
        Raises:
            ZMapInputError: If the file doesn't exist or isn't readable
        """
        if not os.path.isfile(file_path):
            raise ZMapInputError(f"Whitelist file not found: {file_path}")
        if not os.access(file_path, os.R_OK):
            raise ZMapInputError(f"Whitelist file not readable: {file_path}")
        self.whitelist_file = file_path
    
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
    
    def create_blacklist_file(self, subnets: List[str], output_file: str) -> str:
        """
        Create a blacklist file from a list of subnets
        
        Args:
            subnets: List of subnet CIDRs to blacklist
            output_file: Path to save the blacklist file
            
        Returns:
            Path to the created blacklist file
            
        Raises:
            ZMapInputError: If a subnet is invalid or file can't be created
        """
        # Validate subnets
        for subnet in subnets:
            try:
                ipaddress.ip_network(subnet)
            except ValueError as e:
                raise ZMapInputError(f"Invalid subnet in blacklist: {subnet} - {str(e)}")
        
        # Write to file
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(subnets))
        except IOError as e:
            raise ZMapInputError(f"Failed to create blacklist file: {str(e)}")
            
        self.blacklist_file = output_file
        return output_file
    
    def create_whitelist_file(self, subnets: List[str], output_file: str) -> str:
        """
        Create a whitelist file from a list of subnets
        
        Args:
            subnets: List of subnet CIDRs to whitelist
            output_file: Path to save the whitelist file
            
        Returns:
            Path to the created whitelist file
            
        Raises:
            ZMapInputError: If a subnet is invalid or file can't be created
        """
        # Validate subnets
        for subnet in subnets:
            try:
                ipaddress.ip_network(subnet)
            except ValueError as e:
                raise ZMapInputError(f"Invalid subnet in whitelist: {subnet} - {str(e)}")
        
        # Write to file
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(subnets))
        except IOError as e:
            raise ZMapInputError(f"Failed to create whitelist file: {str(e)}")
            
        self.whitelist_file = output_file
        return output_file

    def create_target_file(self, targets: List[str], output_file: str) -> str:
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
                raise ZMapInputError(f"Invalid IP address: {ip} - {str(e)}")
        
        # Write to file
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(targets))
        except IOError as e:
            raise ZMapInputError(f"Failed to create target file: {str(e)}")
            
        self.input_file = output_file
        return output_file
    
    def generate_standard_blacklist(self, output_file: str) -> str:
        """
        Generate a blacklist file with standard private network ranges
        
        Args:
            output_file: Path to save the blacklist file
            
        Returns:
            Path to the created blacklist file
        """
        private_ranges = [
            "10.0.0.0/8",      # RFC1918 private network
            "172.16.0.0/12",   # RFC1918 private network
            "192.168.0.0/16",  # RFC1918 private network
            "127.0.0.0/8",     # Loopback
            "169.254.0.0/16",  # Link-local
            "224.0.0.0/4",     # Multicast
            "240.0.0.0/4",     # Reserved
            "192.0.2.0/24",    # TEST-NET for documentation
            "198.51.100.0/24", # TEST-NET-2 for documentation
            "203.0.113.0/24",  # TEST-NET-3 for documentation
        ]
        
        return self.create_blacklist_file(private_ranges, output_file)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert input configuration to a dictionary for command-line options"""
        result = {}
        
        if self.blacklist_file:
            result["blacklist_file"] = self.blacklist_file
        
        if self.whitelist_file:
            result["whitelist_file"] = self.whitelist_file
            
        if self.input_file:
            result["input_file"] = self.input_file
            
        if self.ignore_blacklist:
            result["ignore_blacklist"] = True
            
        if self.ignore_invalid_hosts:
            result["ignore_invalid_hosts"] = True
            
        if self.target_subnets:
            result["subnets"] = self.target_subnets
            
        return result 