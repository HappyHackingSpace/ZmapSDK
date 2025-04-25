"""
Exceptions for the ZMap SDK
"""


class ZMapError(Exception):
    """Base exception for ZMap SDK errors"""

    pass


class ZMapCommandError(ZMapError):
    """Exception raised when zmap command fails"""

    def __init__(self, command: str, returncode: int, stderr: str):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        message = f"ZMap command failed with return code {returncode}:\nCommand: {command}\nError: {stderr}"
        super().__init__(message)


class ZMapConfigError(ZMapError):
    """Exception raised for configuration errors"""

    pass


class ZMapInputError(ZMapError):
    """Exception raised for input file errors"""

    pass


class ZMapOutputError(ZMapError):
    """Exception raised for output-related errors"""

    pass


class ZMapParserError(ZMapError):
    """Exception raised when parsing ZMap output fails"""

    pass
