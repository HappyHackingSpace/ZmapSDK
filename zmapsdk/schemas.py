from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    target_port: int | None = Field(None, description="Port number to scan")
    subnets: list[str] | None = Field(None, description="List of subnets to scan")
    output_file: str | None = Field(None, description="Output file path")
    blocklist_file: str | None = Field(None, description="Path to blocklist file")
    allowlist_file: str | None = Field(None, description="Path to allowlist file")
    bandwidth: str | None = Field(None, description="Bandwidth cap for scan")
    probe_module: str | None = Field(None, description="Probe module to use")
    rate: int | None = Field(None, description="Packets per second to send")
    seed: int | None = Field(None, description="Random seed")
    verbosity: int | None = Field(None, description="Verbosity level")
    return_results: bool = Field(
        False,
        description="Return results directly in response instead of writing to file",
    )
    # Add other relevant parameters as needed


class ScanResult(BaseModel):
    scan_id: str
    status: str
    ips_found: list[str] | None = None
    output_file: list[str] | None = None
    error: list[str] | None = None


class BlocklistRequest(BaseModel):
    subnets: list[str]
    output_file: str | None = None


class StandardBlocklistRequest(BaseModel):
    output_file: str | None = None


class FileResponse(BaseModel):
    file_path: str
    message: str
