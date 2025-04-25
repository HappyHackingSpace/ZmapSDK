"""
Output handling module for ZMap SDK
"""

import os
from typing import Any

from zmapsdk.exceptions import ZMapOutputError


class ZMapOutput:
    """
    Class for handling ZMap output options
    """

    def __init__(self):
        """Initialize the output handler"""
        self.output_file: str | None = None
        self.output_fields: list[str] | str | None = None
        self.output_module: str | None = None
        self.output_filter: str | None = None
        self.output_args: str | None = None
        self.log_file: str | None = None
        self.log_directory: str | None = None
        self.metadata_file: str | None = None
        self.status_updates_file: str | None = None
        self.verbosity: int | None = None
        self.quiet: bool = False
        self.disable_syslog: bool = False

    def set_output_file(self, file_path: str) -> None:
        """
        Set the output file for scan results

        Args:
            file_path: Path to the output file

        Raises:
            ZMapOutputError: If the directory doesn't exist or isn't writable
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.isdir(directory):
            raise ZMapOutputError(f"Output directory does not exist: {directory}")
        if directory and not os.access(directory, os.W_OK):
            raise ZMapOutputError(f"Output directory is not writable: {directory}")
        self.output_file = file_path

    def set_output_fields(self, fields: list[str] | str) -> None:
        """
        Set the output fields to include in results

        Args:
            fields: List of field names or comma-separated string of field names
        """
        self.output_fields = fields

    def set_output_module(self, module: str) -> None:
        """
        Set the output module

        Args:
            module: Name of the output module
        """
        self.output_module = module

    def set_output_filter(self, filter_expr: str) -> None:
        """
        Set a filter for output results

        Args:
            filter_expr: Filter expression
        """
        self.output_filter = filter_expr

    def set_log_file(self, file_path: str) -> None:
        """
        Set the log file

        Args:
            file_path: Path to the log file

        Raises:
            ZMapOutputError: If the directory doesn't exist or isn't writable
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.isdir(directory):
            raise ZMapOutputError(f"Log directory does not exist: {directory}")
        if directory and not os.access(directory, os.W_OK):
            raise ZMapOutputError(f"Log directory is not writable: {directory}")
        self.log_file = file_path

    def set_log_directory(self, directory: str) -> None:
        """
        Set the log directory for timestamped logs

        Args:
            directory: Path to the log directory

        Raises:
            ZMapOutputError: If the directory doesn't exist or isn't writable
        """
        if not os.path.isdir(directory):
            raise ZMapOutputError(f"Log directory does not exist: {directory}")
        if not os.access(directory, os.W_OK):
            raise ZMapOutputError(f"Log directory is not writable: {directory}")
        self.log_directory = directory

    def set_metadata_file(self, file_path: str) -> None:
        """
        Set the metadata output file

        Args:
            file_path: Path to the metadata file

        Raises:
            ZMapOutputError: If the directory doesn't exist or isn't writable
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.isdir(directory):
            raise ZMapOutputError(f"Metadata directory does not exist: {directory}")
        if directory and not os.access(directory, os.W_OK):
            raise ZMapOutputError(f"Metadata directory is not writable: {directory}")
        self.metadata_file = file_path

    def set_status_updates_file(self, file_path: str) -> None:
        """
        Set the status updates file

        Args:
            file_path: Path to the status updates file

        Raises:
            ZMapOutputError: If the directory doesn't exist or isn't writable
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.isdir(directory):
            raise ZMapOutputError(
                f"Status updates directory does not exist: {directory}",
            )
        if directory and not os.access(directory, os.W_OK):
            raise ZMapOutputError(
                f"Status updates directory is not writable: {directory}",
            )
        self.status_updates_file = file_path

    def set_verbosity(self, level: int) -> None:
        """
        Set the verbosity level

        Args:
            level: Verbosity level (0-5)

        Raises:
            ZMapOutputError: If the level is out of range
        """
        if not 0 <= level <= 5:
            raise ZMapOutputError(
                f"Verbosity level must be between 0 and 5, got {level}",
            )
        self.verbosity = level

    def enable_quiet_mode(self) -> None:
        """Enable quiet mode (no status updates)"""
        self.quiet = True

    def disable_quiet_mode(self) -> None:
        """Disable quiet mode"""
        self.quiet = False

    def enable_syslog(self) -> None:
        """Enable syslog logging"""
        self.disable_syslog = False

    def disable_syslog_logging(self) -> None:
        """Disable syslog logging"""
        self.disable_syslog = True

    def to_dict(self) -> dict[str, Any]:
        """Convert output configuration to a dictionary for command-line options"""
        result = {}

        if self.output_file:
            result["output_file"] = self.output_file

        if self.output_fields:
            result["output_fields"] = self.output_fields

        if self.output_module:
            result["output_module"] = self.output_module

        if self.output_filter:
            result["output_filter"] = self.output_filter

        if self.output_args:
            result["output_args"] = self.output_args

        if self.log_file:
            result["log_file"] = self.log_file

        if self.log_directory:
            result["log_directory"] = self.log_directory

        if self.metadata_file:
            result["metadata_file"] = self.metadata_file

        if self.status_updates_file:
            result["status_updates_file"] = self.status_updates_file

        if self.verbosity is not None:
            result["verbosity"] = self.verbosity

        if self.quiet:
            result["quiet"] = True

        if self.disable_syslog:
            result["disable_syslog"] = True

        return result

    @staticmethod
    def get_common_output_fields() -> dict[str, str]:
        """
        Get a dictionary of common output fields and their descriptions

        Returns:
            Dictionary mapping field names to descriptions
        """
        return {
            "saddr": "Source IP address",
            "daddr": "Destination IP address",
            "sport": "Source port",
            "dport": "Destination port",
            "seqnum": "TCP sequence number",
            "acknum": "TCP acknowledgement number",
            "window": "TCP window",
            "classification": "Response classification (e.g., synack, rst)",
            "success": "Whether the probe was successful",
            "repeat": "Whether this response is a repeat",
            "cooldown": "Cooldown time in seconds",
            "timestamp_ts": "Timestamp in seconds",
            "timestamp_us": "Microsecond component of timestamp",
            "icmp_type": "ICMP type",
            "icmp_code": "ICMP code",
            "icmp_unreach_str": "ICMP unreachable string",
            "data": "Application response data",
            "ttl": "Time to live",
        }
