from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from starlette.testclient import TestClient

from zmapsdk.api import app


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    """Fixture that provides a test client for FastAPI"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def mock_zmap() -> Generator[MagicMock, Any, None]:
    """Automatically mock the ZMap instance before each test."""
    with patch("zmapsdk.api.ZMap") as mock_zmap:
        mock_instance = MagicMock()
        mock_zmap.return_value = mock_instance
        app.state.zmap = mock_instance
        yield mock_instance
        if hasattr(app.state, "zmap"):
            del app.state.zmap


@pytest.fixture(autouse=True)
def setup_teardown() -> Generator[None, Any, None]:
    """Fixture to handle setup and teardown for each test."""
    mock_zmap = MagicMock()
    app.state.zmap = mock_zmap
    yield
    # Teardown - clean up
    if hasattr(app.state, "zmap"):
        del app.state.zmap


def test_root_endpoint_success(
    client: TestClient, mock_zmap: Generator[MagicMock, Any, None]
) -> None:
    """Test the root endpoint with successful ZMap version check."""
    mock_zmap.get_version.return_value = "zmap 3.0.0"

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "ZMap SDK API",
        "version": "zmap 3.0.0",
        "description": "REST API for ZMap network scanner",
    }
    mock_zmap.get_version.assert_called_once()


def test_api_docs_endpoints(client: TestClient) -> None:
    """Test that api documentation endpoints exist."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()

    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui" in response.text

    response = client.get("/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text
