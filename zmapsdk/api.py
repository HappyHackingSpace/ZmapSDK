import os
import tempfile
from contextlib import asynccontextmanager

import psutil
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse as StarletteFileResponse

from zmapsdk.schemas import (
    BlocklistRequest,
    FileResponse,
    ScanRequest,
    ScanResult,
    StandardBlocklistRequest,
)

from .core import ZMap

# Scan tracking dictionary
active_scans = {}


# Initialize ZMap instance for API
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize ZMap on startup
    app.state.zmap = ZMap()
    yield
    # Clean up on shutdown (if needed)


# Initialize FastAPI
app = FastAPI(
    title="ZMap SDK API",
    description="REST API for ZMap network scanner",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Info"])
async def root():
    """API root endpoint with basic information"""
    return {
        "name": "ZMap SDK API",
        "version": app.state.zmap.get_version(),
        "description": "REST API for ZMap network scanner",
    }


@app.get("/probe-modules", tags=["Info"], response_model=list[str])
async def get_probe_modules():
    """Get available probe modules"""
    return app.state.zmap.get_probe_modules()


@app.get("/output-modules", tags=["Info"], response_model=list[str])
async def get_output_modules():
    """Get available output modules"""
    return app.state.zmap.get_output_modules()


@app.get("/output-fields", tags=["Info"], response_model=list[str])
async def get_output_fields(probe_module: str | None = None):
    """Get available output fields for a probe module"""
    return app.state.zmap.get_output_fields(probe_module)


@app.get("/interfaces", tags=["Info"], response_model=list[str])
async def get_interfaces():
    """Get available network interfaces"""
    return [iface for iface in psutil.net_if_addrs().keys()]


@app.post("/blocklist", tags=["Input"])
async def create_blocklist(request: BlocklistRequest) -> FileResponse:
    """Create a blocklist file from a list of subnets"""
    try:
        # Use provided output file or create temporary one
        output_file = request.output_file
        if not output_file:
            temp_fd, output_file = tempfile.mkstemp(
                prefix="zmap_blocklist_",
                suffix=".txt",
            )
            os.close(temp_fd)

        file_path = app.state.zmap.create_blocklist_file(request.subnets, output_file)

        return FileResponse(
            file_path=file_path,
            message=f"Blocklist file created with {len(request.subnets)} subnets",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/standard-blocklist", tags=["Input"])
async def generate_standard_blocklist(
    request: StandardBlocklistRequest,
) -> FileResponse:
    """Generate a standard blocklist file"""
    try:
        # Use provided output file or create temporary one
        output_file = request.output_file
        if not output_file:
            temp_fd, output_file = tempfile.mkstemp(
                prefix="zmap_std_blocklist_",
                suffix=".txt",
            )
            os.close(temp_fd)

        file_path = app.state.zmap.generate_standard_blocklist(output_file)

        return FileResponse(
            file_path=file_path, message="Standard blocklist file created"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/allowlist", tags=["Input"])
async def create_allowlist(request: BlocklistRequest) -> FileResponse:
    """Create an allowlist file from a list of subnets"""
    try:
        # Use provided output file or create temporary one
        output_file = request.output_file
        if not output_file:
            temp_fd, output_file = tempfile.mkstemp(
                prefix="zmap_allowlist_",
                suffix=".txt",
            )
            os.close(temp_fd)

        file_path = app.state.zmap.create_allowlist_file(request.subnets, output_file)

        return FileResponse(
            file_path=file_path,
            message=f"Allowlist file created with {len(request.subnets)} subnets",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan-sync", tags=["Scan"], response_model=ScanResult)
async def sync_scan(scan_request: ScanRequest):
    """Run a ZMap scan synchronously and return results directly"""
    # Set default output file if not provided
    output_file = scan_request.output_file
    if not output_file:
        temp_fd, output_file = tempfile.mkstemp(prefix="zmap_api_", suffix=".txt")
        os.close(temp_fd)

    try:
        # Convert model to dict and remove None values
        params = {
            k: v
            for k, v in scan_request.dict().items()
            if v is not None and k != "return_results"
        }

        # Ensure output file is set
        params["output_file"] = output_file

        # Run scan synchronously
        results = app.state.zmap.scan(**params)

        # Return results directly
        return ScanResult(
            scan_id="direct_scan",
            status="completed",
            ips_found=results,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class APIServer:
    """
    Server class for running the ZMap SDK API
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize the API server

        Args:
            host: Host to bind the server to
            port: Port to bind the server to
        """
        self.host = host
        self.port = port
        self.app = app

    def run(self):
        """
        Run the API server
        """
        uvicorn.run(app, host=self.host, port=self.port)
