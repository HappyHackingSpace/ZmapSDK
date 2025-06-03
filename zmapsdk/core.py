"""
Core module for ZMap SDK
"""

from collections.abc import Callable
from typing import Any

from zmapsdk.config import ZMapScanConfig
from zmapsdk.input import ZMapInput
from zmapsdk.output import ZMapOutput
from zmapsdk.parser import ZMapParser
from zmapsdk.runner import ZMapRunner


# Option categories for ZMap configuration
class ZMapOptionCategories:
    """Configuration option categories for ZMap"""

    INPUT_OPTIONS = frozenset(
        {
            "blocklist_file",
            "allowlist_file",
            "input_file",
            "ignore_blocklist",
            "ignore_invalid_hosts",
        },
    )

    OUTPUT_OPTIONS = frozenset(
        {
            "output_fields",
            "output_module",
            "output_filter",
            "output_args",
            "log_file",
            "log_directory",
            "metadata_file",
            "status_updates_file",
            "verbosity",
            "quiet",
            "disable_syslog",
        },
    )


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

    def scan(
        self,
        target_port: int | None = None,
        subnets: list[str] | None = None,
        output_file: str | None = None,
        callback: Callable[[str], None] | None = None,
        **kwargs: Any,
    ) -> list[str]:
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
        # Initialize scan configurations
        scan_config = ZMapScanConfig()
        scan_input = ZMapInput()
        scan_output = ZMapOutput()

        # Set core scan parameters
        if target_port is not None:
            scan_config.target_port = target_port

        if subnets:
            scan_input.add_subnets(subnets)

        if output_file:
            scan_output.set_output_file(output_file)

        # Distribute additional parameters to appropriate configuration objects
        self._process_scan_options(kwargs, scan_config, scan_input, scan_output)

        # Execute the scan
        return self.runner.scan(
            config=scan_config,
            input_config=scan_input,
            output_config=scan_output,
            callback=callback,
        )

    @staticmethod
    def _process_scan_options(
        options: dict[str, Any],
        scan_config: ZMapScanConfig,
        scan_input: ZMapInput,
        scan_output: ZMapOutput,
    ) -> None:
        """
        Process and distribute scan options to appropriate configuration objects.

        Args:
            options: Dictionary of scan options
            scan_config: ZMap scan configuration object
            scan_input: ZMap input configuration object
            scan_output: ZMap output configuration object
        """
        for key, value in options.items():
            if key in ZMapOptionCategories.INPUT_OPTIONS:
                setattr(scan_input, key, value)
            elif key in ZMapOptionCategories.OUTPUT_OPTIONS:
                setattr(scan_output, key, value)
            else:
                setattr(scan_config, key, value)

    def run(self, **kwargs: Any) -> tuple[int, str, str]:
        """
        Run ZMap with the specified parameters

        Args:
            **kwargs: Command-line options as keyword arguments

        Returns:
            Tuple of (return code, stdout, stderr)
        """
        return self.runner.run_command(**kwargs)

    def get_probe_modules(self) -> list[str]:
        """
        Get list of available probe modules

        Returns:
            List of available probe module names
        """
        return self.runner.get_probe_modules()

    def get_output_modules(self) -> list[str]:
        """
        Get list of available output modules

        Returns:
            List of available output module names
        """
        return self.runner.get_output_modules()

    def get_output_fields(self, probe_module: str | None = None) -> list[str]:
        """
        Get list of available output fields for the specified probe module

        Args:
            probe_module: Probe module to get output fields for (optional)

        Returns:
            List of available output field names
        """
        return self.runner.get_output_fields(probe_module)

    def get_interfaces(self) -> list[str]:
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

    def blocklist_from_file(self, blocklist_file: str) -> None:
        """
        Validate and use a blocklist file

        Args:
            blocklist_file: Path to the blocklist file
        """
        self.input.set_blocklist_file(blocklist_file)

    def allowlist_from_file(self, allowlist_file: str) -> None:
        """
        Validate and use a allowlist file

        Args:
            allowlist_file: Path to the allowlist file
        """
        self.input.set_allowlist_file(allowlist_file)

    def create_blocklist_file(self, subnets: list[str], output_file: str) -> str:
        """
        Create a blocklist file from a list of subnets

        Args:
            subnets: List of subnet CIDRs to blocklist
            output_file: Path to save the blocklist file

        Returns:
            Path to the created blocklist file
        """
        return self.input.create_blocklist_file(subnets, output_file)

    def create_allowlist_file(self, subnets: list[str], output_file: str) -> str:
        """
        Create a allowlist file from a list of subnets

        Args:
            subnets: List of subnet CIDRs to allowlist
            output_file: Path to save the allowlist file

        Returns:
            Path to the created allowlist file
        """
        return self.input.create_allowlist_file(subnets, output_file)

    def create_target_file(self, targets: list[str], output_file: str) -> str:
        """
        Create an input file for specific target IPs

        Args:
            targets: List of IP addresses to scan
            output_file: Path to save the input file

        Returns:
            Path to the created input file
        """
        return self.input.create_target_file(targets, output_file)

    def generate_standard_blocklist(self, output_file: str) -> str:
        """
        Generate a blocklist file with standard private network ranges

        Args:
            output_file: Path to save the blocklist file

        Returns:
            Path to the created blocklist file
        """
        return self.input.generate_standard_blocklist(output_file)

    def parse_results(
        self,
        file_path: str,
        fields: list[str] | None = None,
    ) -> list[dict[str, str]]:
        """
        Parse scan results from a file

        Args:
            file_path: Path to the results file
            fields: List of field names (if not provided, will try to read from header)

        Returns:
            List of dictionaries, each representing a row with field names as keys
        """
        return ZMapParser.parse_csv_results(file_path, fields)

    def parse_metadata(self, file_path: str) -> dict[str, Any]:
        """
        Parse a ZMap metadata file

        Args:
            file_path: Path to the metadata file

        Returns:
            Dictionary containing metadata
        """
        return ZMapParser.parse_metadata(file_path)

    def extract_ips(
        self,
        results: list[dict[str, Any]],
        ip_field: str = "saddr",
    ) -> list[str]:
        """
        Extract IP addresses from parsed results

        Args:
            results: List of result dictionaries
            ip_field: Field name containing IP addresses

        Returns:
            List of IP addresses
        """
        return ZMapParser.extract_ips(results, ip_field)

    def stream_results(self, file_path: str, fields: list[str] | None = None):
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
