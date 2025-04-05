"""
conftest.py
===========

Contains pytest fixtures for setting up and tearing down
resources used in testing the db_client module.
"""

from unittest.mock import MagicMock, patch

import pytest
from darca_log_facility.logger import DarcaLogger

from darca_vector_db import DBClient, QdrantDBClient


@pytest.fixture(scope="module")
def mock_logger():
    """
    Provides a mock logger to prevent actual logging during tests.
    """
    with patch.object(DarcaLogger, "get_logger", return_value=MagicMock()):
        yield


@pytest.fixture(scope="module")
def qdrant_client(mock_logger):
    """
    Fixture to create a QdrantDBClient instance for testing with
    mocked methods.
    """
    client = QdrantDBClient(host="localhost", port=6333)
    client.client = MagicMock()  # Mock the actual Qdrant client
    client.logger = MagicMock()  # Mock the logger
    return client


@pytest.fixture(scope="module")
def db_client(mock_logger):
    """
    Fixture to create a generic DBClient instance for testing with
    mocked Qdrant backend.
    """
    client = DBClient(backend="qdrant")
    client._client = MagicMock()
    client.logger = MagicMock()
    return client
