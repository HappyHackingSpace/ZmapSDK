"""
Core module for ZMap SDK
"""

import os
import tempfile
from typing import List, Dict, Any, Optional, Union, Tuple, Callable

from .config import ZMapScanConfig
from .input import ZMapInput
from .output import ZMapOutput
from .runner import ZMapRunner
from .parser import ZMapParser
from .exceptions import ZMapError, ZMapCommandError


class ZMap:
    """
    Main class for the ZMap SDK
    """
    
    def __init__(self, zmap_path: str = "zmap"):
        """
        Initialize the ZMap SDK
        
        Args:
            zmap_path: Path to the zmap executable (defaults to "zmap", assuming it's in PATH)
        """
        self.runner = ZMapRunner(zmap_path)
        self.config = ZMapScanConfig()
        self.input = ZMapInput()
        self.output = ZMapOutput()
    
    def scan(self, 
            target_port: Optional[int] = None,
            subnets: Optional[List[str]] = None,
            output_file: Optional[str] = None,
            callback: Optional[Callable[[str], None]] = None,
            **kwargs) -> List[str]:
        """
        Perform a scan and return the results
        
        Args:
            target_port: Port number to scan
            subnets: List of subnets to scan (defaults to scanning the internet)
            output_file: Output file (if not specified, a temporary file will be used)
            callback: Optional callback function for real-time output
            **kwargs: Additional parameters to pass to ZMap
            
        Returns:
            List of IP addresses that responded
        """
        # Create a new configuration for this scan
        scan_config = ZMapScanConfig()
        scan_input = ZMapInput()
        scan_output = ZMapOutput()
        
        # Set target port
        if target_port is not None:
            scan_config.target_port = target_port
            
        # Set subnets
        if subnets:
            scan_input.add_subnets(subnets)
            
        # Set output file
        if output_file:
            scan_output.set_output_file(output_file)
        
        # Process other parameters and assign them to the appropriate config object
        for key, value in kwargs.items():
            # Input options
            if key in ['blacklist_file', 'whitelist_file', 'input_file', 'ignore_blacklist', 'ignore_invalid_hosts']:
                setattr(scan_input, key, value)
            # Output options
            elif key in ['output_fields', 'output_module', 'output_filter', 'output_args',
                        'log_file', 'log_directory', 'metadata_file', 'status_updates_file',
                        'verbosity', 'quiet', 'disable_syslog']:
                setattr(scan_output, key, value)
            # Config options (everything else)
            else:
                setattr(scan_config, key, value)
        
        # Run the scan
        return self.runner.scan(
            config=scan_config,
            input_config=scan_input,
            output_config=scan_output,
            callback=callback
        )
    
    def run(self, **kwargs) -> Tuple[int, str, str]:
        """
        Run ZMap with the specified parameters
        
        Args:
            **kwargs: Command-line options as keyword arguments
            
        Returns:
            Tuple of (return code, stdout, stderr)
        """
        return self.runner.run_command(**kwargs)
    
    def get_probe_modules(self) -> List[str]:
        """
        Get list of available probe modules
        
        Returns:
            List of available probe module names
        """
        return self.runner.get_probe_modules()
    
    def get_output_modules(self) -> List[str]:
        """
        Get list of available output modules
        
        Returns:
            List of available output module names
        """
        return self.runner.get_output_modules()
    
    def get_output_fields(self, probe_module: Optional[str] = None) -> List[str]:
        """
        Get list of available output fields for the specified probe module
        
        Args:
            probe_module: Probe module to get output fields for (optional)
            
        Returns:
            List of available output field names
        """
        return self.runner.get_output_fields(probe_module)

    def get_interfaces(self) -> List[str]:
        """
        Get list of available network interfaces
        
        Returns:
            List of available interface names
        """
        return self.runner.get_interfaces()
    
    def get_version(self) -> str:
        """
        Get ZMap version
        
        Returns:
            Version string
        """
        return self.runner.get_version()
    
    def blacklist_from_file(self, blacklist_file: str) -> None:
        """
        Validate and use a blacklist file
        
        Args:
            blacklist_file: Path to the blacklist file
        """
        self.input.set_blacklist_file(blacklist_file)

    def whitelist_from_file(self, whitelist_file: str) -> None:
        """
        Validate and use a whitelist file
        
        Args:
            whitelist_file: Path to the whitelist file
        """
        self.input.set_whitelist_file(whitelist_file)

    def create_blacklist_file(self, subnets: List[str], output_file: str) -> str:
        """
        Create a blacklist file from a list of subnets
        
        Args:
            subnets: List of subnet CIDRs to blacklist
            output_file: Path to save the blacklist file
            
        Returns:
            Path to the created blacklist file
        """
        return self.input.create_blacklist_file(subnets, output_file)

    def create_whitelist_file(self, subnets: List[str], output_file: str) -> str:
        """
        Create a whitelist file from a list of subnets
        
        Args:
            subnets: List of subnet CIDRs to whitelist
            output_file: Path to save the whitelist file
            
        Returns:
            Path to the created whitelist file
        """
        return self.input.create_whitelist_file(subnets, output_file)
        
    def create_target_file(self, targets: List[str], output_file: str) -> str:
        """
        Create an input file for specific target IPs
        
        Args:
            targets: List of IP addresses to scan
            output_file: Path to save the input file
            
        Returns:
            Path to the created input file
        """
        return self.input.create_target_file(targets, output_file)
    
    def generate_standard_blacklist(self, output_file: str) -> str:
        """
        Generate a blacklist file with standard private network ranges
        
        Args:
            output_file: Path to save the blacklist file
            
        Returns:
            Path to the created blacklist file
        """
        return self.input.generate_standard_blacklist(output_file)
    
    def parse_results(self, file_path: str, fields: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        Parse scan results from a file
        
        Args:
            file_path: Path to the results file
            fields: List of field names (if not provided, will try to read from header)
            
        Returns:
            List of dictionaries, each representing a row with field names as keys
        """
        return ZMapParser.parse_csv_results(file_path, fields)
    
    def parse_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a ZMap metadata file
        
        Args:
            file_path: Path to the metadata file
            
        Returns:
            Dictionary containing metadata
        """
        return ZMapParser.parse_metadata(file_path)
    
    def extract_ips(self, results: List[Dict[str, Any]], ip_field: str = 'saddr') -> List[str]:
        """
        Extract IP addresses from parsed results
        
        Args:
            results: List of result dictionaries
            ip_field: Field name containing IP addresses
            
        Returns:
            List of IP addresses
        """
        return ZMapParser.extract_ips(results, ip_field)
    
    def stream_results(self, file_path: str, fields: Optional[List[str]] = None):
        """
        Stream results from a file without loading everything into memory
        
        Args:
            file_path: Path to the results file
            fields: List of field names (if not provided, will try to read from header)
            
        Returns:
            Iterator yielding dictionaries, each representing a row with field names as keys
        """
        return ZMapParser.stream_results(file_path, fields)
    
    def count_results(self, file_path: str) -> int:
        """
        Count the number of results in a file
        
        Args:
            file_path: Path to the results file
            
        Returns:
            Number of result rows
        """
        return ZMapParser.count_results(file_path) 