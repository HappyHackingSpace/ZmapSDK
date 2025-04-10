"""
Command-line interface for ZMap SDK
"""

import argparse
import sys
import logging
from typing import List, Optional

from .api import APIServer
from .core import ZMap


def run_api_server(args: argparse.Namespace) -> int:
    """Run the API server with the specified options"""
    try:
        # Configure logging
        log_level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create and run API server
        server = APIServer(host=args.host, port=args.port)
        print(f"Starting ZMap SDK API server on http://{args.host}:{args.port}")
        print(f"API documentation available at http://{args.host}:{args.port}/docs")
        server.run()
        
        return 0
    except Exception as e:
        print(f"Error starting API server: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="ZMap SDK command-line interface")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # API server command
    api_parser = subparsers.add_parser("api", help="Run the ZMap SDK API server")
    api_parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    api_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    api_parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    # Parse arguments
    args = parser.parse_args(argv)
    
    # Check ZMap version (for all commands)
    if args.command:
        try:
            zmap = ZMap()
            print(f"ZMap version: {zmap.get_version()}")
        except Exception as e:
            print(f"Warning: Could not detect ZMap version: {e}", file=sys.stderr)
    
    # Run appropriate command
    if args.command == "api":
        return run_api_server(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main()) 