"""
ZMap SDK - Python SDK for the ZMap network scanner
"""

from pathlib import Path

import tomli

from .zmapsdk import ZMap, ZMapCommandError, ZMapError

# read version from pyproject.toml
try:
    _PYPROJECT_PATH = Path(__file__).parent.parent / "pyproject.toml"
    with open(_PYPROJECT_PATH, "rb") as f:
        _PYPROJECT = tomli.load(f)
        __version__ = _PYPROJECT["project"]["version"]
except (FileNotFoundError, KeyError, tomli.TOMLDecodeError):
    # fallback for something went wrong
    __version__ = "0.0.0"

__all__ = ["ZMap", "ZMapError", "ZMapCommandError"]
