"""
Runner module for ZMap SDK
"""

import os
import subprocess
import tempfile
from collections.abc import Callable

from zmapsdk.config import ZMapScanConfig
from zmapsdk.exceptions import ZMapCommandError
from zmapsdk.input import ZMapInput
from zmapsdk.output import ZMapOutput


class ZMapRunner:
    """
    Class for running ZMap commands
    """

    def __init__(self, zmap_path: str = "zmap"):
        """
        Initialize the ZMap runner

        Args:
            zmap_path: Path to the zmap executable (defaults to "zmap", assuming it's in PATH)
        """
        self.zmap_path = zmap_path
        self._check_zmap_exists()

    def _check_zmap_exists(self) -> None:
        """Check if zmap executable exists and is accessible"""
        try:
            subprocess.run(
                [self.zmap_path, "--version"],
                capture_output=True,
                check=True,
            )
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            raise ZMapCommandError(command=self.zmap_path, returncode=-1, stderr=str(e))

    def _build_command(self, **kwargs) -> list[str]:
        """
        Build zmap command from parameters

        Args:
            **kwargs: Command-line options as keyword arguments

        Returns:
            List of command parts
        """
        cmd = [self.zmap_path]

        # Process all the parameters
        for key, value in kwargs.items():
            if value is None:
                continue

            # Convert underscores to hyphens for flags
            key = key.replace("_", "-")

            # Boolean flags
            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{key}")
            # Lists (for subnets)
            elif isinstance(value, list):
                if key == "subnets":
                    cmd.extend(value)
                else:
                    cmd.append(f"--{key}={','.join(map(str, value))}")
            # All other parameters
            else:
                cmd.append(f"--{key}={value}")

        return cmd

    def run_command(
        self,
        config: ZMapScanConfig | None = None,
        input_config: ZMapInput | None = None,
        output_config: ZMapOutput | None = None,
        capture_output: bool = True,
        callback: Callable[[str], None] | None = None,
        **kwargs,
    ) -> tuple[int, str, str]:
        """
        Run a ZMap command with the specified parameters

        Args:
            config: Configuration object
            input_config: Input configuration object
            output_config: Output configuration object
            capture_output: Whether to capture and return command output
            callback: Optional callback function for real-time output
            **kwargs: Additional parameters to pass to zmap

        Returns:
            Tuple of (return code, stdout, stderr)
        """
        # Combine all parameters
        combined_params = {}

        # Add config parameters if provided
        if config:
            combined_params.update(config.to_dict())

        # Add input parameters if provided
        if input_config:
            combined_params.update(input_config.to_dict())

        # Add output parameters if provided
        if output_config:
            combined_params.update(output_config.to_dict())

        # Add any additional parameters
        combined_params.update(kwargs)

        # Build command
        cmd = self._build_command(**combined_params)

        # Run command
        try:
            if callback:
                # Use Popen for real-time output with callback
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE if capture_output else None,
                    stderr=subprocess.PIPE if capture_output else None,
                    text=True,
                    bufsize=1,  # Line buffered
                )

                stdout_data = []
                stderr_data = []

                # Read and process stdout in real-time
                if process.stdout:
                    for line in iter(process.stdout.readline, ""):
                        if not line:
                            break
                        stdout_data.append(line)
                        callback(line)

                # Read stderr
                if process.stderr:
                    for line in iter(process.stderr.readline, ""):
                        if not line:
                            break
                        stderr_data.append(line)

                process.wait()

                return process.returncode, "".join(stdout_data), "".join(stderr_data)

            elif capture_output:
                # Simple execution with output capture
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                return result.returncode, result.stdout, result.stderr

            else:
                # Just run the command without capturing output
                result = subprocess.run(cmd, check=False)
                return result.returncode, "", ""

        except subprocess.SubprocessError as e:
            raise ZMapCommandError(command=" ".join(cmd), returncode=-1, stderr=str(e))

    def scan(
        self,
        config: ZMapScanConfig | None = None,
        input_config: ZMapInput | None = None,
        output_config: ZMapOutput | None = None,
        temp_output_file: bool = False,
        callback: Callable[[str], None] | None = None,
        **kwargs,
    ) -> list[str]:
        """
        Perform a scan and return the results

        Args:
            config: Configuration object
            input_config: Input configuration object
            output_config: Output configuration object
            temp_output_file: Whether to use a temporary output file
            callback: Optional callback function for real-time output
            **kwargs: Additional parameters to pass to zmap

        Returns:
            List of IP addresses that responded
        """
        # Ensure we have an output configuration
        if output_config is None:
            output_config = ZMapOutput()

        # Create temporary output file if requested
        temp_file = None
        try:
            if temp_output_file or not output_config.output_file:
                temp_fd, temp_file = tempfile.mkstemp(prefix="zmap_", suffix=".txt")
                os.close(temp_fd)  # Close the file descriptor
                output_config.set_output_file(temp_file)

            # Set default output module and fields if not specified
            if not output_config.output_module:
                output_config.set_output_module("csv")
            if not output_config.output_fields:
                output_config.set_output_fields("saddr")
            if not output_config.output_filter and output_config.output_module == "csv":
                output_config.set_output_filter("success = 1 && repeat = 0")

            # Run the scan
            returncode, stdout, stderr = self.run_command(
                config=config,
                input_config=input_config,
                output_config=output_config,
                callback=callback,
                **kwargs,
            )

            if returncode != 0:
                raise ZMapCommandError(
                    command=" ".join(
                        self._build_command(
                            **(config.to_dict() if config else {}),
                            **(input_config.to_dict() if input_config else {}),
                            **(output_config.to_dict() if output_config else {}),
                            **kwargs,
                        ),
                    ),
                    returncode=returncode,
                    stderr=stderr,
                )

            # Read results from file
            with open(output_config.output_file) as f:
                results = [line.strip() for line in f if line.strip()]

            return results

        finally:
            # Clean up the temporary file if we created one
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except OSError:
                    pass

    def get_probe_modules(self) -> list[str]:
        """
        Get list of available probe modules

        Returns:
            List of available probe module names
        """
        returncode, stdout, stderr = self.run_command(list_probe_modules=True)
        if returncode != 0:
            raise ZMapCommandError(
                command=f"{self.zmap_path} --list-probe-modules",
                returncode=returncode,
                stderr=stderr,
            )

        # Parse output to extract module names
        modules = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line or line.startswith("Available"):
                continue
            # Typically the output has name then description, split on first space
            parts = line.split(None, 1)
            if parts:
                modules.append(parts[0])

        return modules

    def get_output_modules(self) -> list[str]:
        """
        Get list of available output modules

        Returns:
            List of available output module names
        """
        returncode, stdout, stderr = self.run_command(list_output_modules=True)
        if returncode != 0:
            raise ZMapCommandError(
                command=f"{self.zmap_path} --list-output-modules",
                returncode=returncode,
                stderr=stderr,
            )

        # Parse output to extract module names
        modules = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line or line.startswith("Available"):
                continue
            # Typically the output has name then description, split on first space
            parts = line.split(None, 1)
            if parts:
                modules.append(parts[0])

        return modules

    def get_output_fields(self, probe_module: str | None = None) -> list[str]:
        """
        Get list of available output fields for the specified probe module

        Args:
            probe_module: Probe module to get output fields for (optional)

        Returns:
            List of available output field names
        """
        cmd = {"list_output_fields": True}
        if probe_module:
            cmd["probe_module"] = probe_module

        returncode, stdout, stderr = self.run_command(**cmd)
        if returncode != 0:
            raise ZMapCommandError(
                command=f"{self.zmap_path} --list-output-fields",
                returncode=returncode,
                stderr=stderr,
            )

        # Parse output to extract field names
        fields = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line or line.startswith("Available"):
                continue
            # Typically the output has name then description, split on first space
            parts = line.split(None, 1)
            if parts:
                fields.append(parts[0])

        return fields

    def get_interfaces(self) -> list[str]:
        """
        Get list of available network interfaces

        Returns:
            List of available interface names
        """
        try:
            # Using psutil to get network interfaces
            import psutil

            return [iface for iface in psutil.net_if_addrs().keys()]
        except ImportError:
            # Fallback to socket for basic interface detection
            import platform
            import socket
            import subprocess

            os_name = platform.system().lower()
            interfaces = []

            # Get interfaces based on the operating system
            if os_name == "linux" or os_name == "darwin":
                # Use ifconfig on Unix-like systems
                try:
                    proc = subprocess.run(
                        ["ifconfig", "-a"],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if proc.returncode == 0:
                        for line in proc.stdout.splitlines():
                            if ": " in line:
                                # Extract interface name (like eth0, wlan0, etc.)
                                interfaces.append(line.split(": ")[0])
                except (subprocess.SubprocessError, FileNotFoundError):
                    pass
            elif os_name == "windows":
                # Use ipconfig on Windows
                try:
                    proc = subprocess.run(
                        ["ipconfig"],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if proc.returncode == 0:
                        for line in proc.stdout.splitlines():
                            if "adapter" in line.lower():
                                # Extract adapter name
                                adapter_name = line.split(":", 1)[0].strip()
                                if adapter_name:
                                    interfaces.append(adapter_name)
                except (subprocess.SubprocessError, FileNotFoundError):
                    pass

            # If we still don't have interfaces, try to get the hostname
            if not interfaces:
                # At minimum, return the hostname interface
                interfaces.append(socket.gethostname())

            return interfaces

    def get_version(self) -> str:
        """
        Get ZMap version

        Returns:
            Version string
        """
        returncode, stdout, stderr = self.run_command(version=True)
        if returncode != 0:
            raise ZMapCommandError(
                command=f"{self.zmap_path} --version",
                returncode=returncode,
                stderr=stderr,
            )

        # Extract version from output
        for line in stdout.splitlines():
            line = line.strip()
            if "zmap version" in line.lower():
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.lower() == "version" and i + 1 < len(parts):
                        return parts[i + 1]

        # If we couldn't parse the version, return the first line of output
        return stdout.splitlines()[0].strip() if stdout else "Unknown version"
