"""
test_db_client.py
=================

Tests for the db_client module ensuring 100% coverage.
"""

from unittest.mock import MagicMock, patch

import pytest
from qdrant_client.http.exceptions import UnexpectedResponse

from darca_vector_db import (
    BaseDBClient,
    CollectionCreationError,
    DBClient,
    DBConnectionError,
    VectorInsertionError,
    VectorSearchError,
)


class DummyDBClient(BaseDBClient):
    """
    Dummy implementation of BaseDBClient for testing abstract
    method invocation.
    """

    def connect(self) -> None:
        super().connect()

    def create_collection(
        self, name: str, vector_size: int, distance_metric: str
    ) -> None:
        super().create_collection(name, vector_size, distance_metric)

    def insert_vector(
        self,
        collection_name: str,
        vector_id: str,
        vector: list,
        metadata: dict = None,
    ) -> None:
        super().insert_vector(collection_name, vector_id, vector, metadata)

    def search_vectors(
        self, collection_name: str, query_vector: list, top_k: int = 10
    ) -> None:
        super().search_vectors(collection_name, query_vector, top_k)


def test_base_dbclient_connect():
    """
    Test that BaseDBClient.connect() raises NotImplementedError.
    """
    client = DummyDBClient()
    with pytest.raises(
        NotImplementedError, match="Subclasses must implement this method."
    ):
        client.connect()


def test_base_dbclient_create_collection():
    """
    Test that BaseDBClient.create_collection() raises NotImplementedError.
    """
    client = DummyDBClient()
    with pytest.raises(
        NotImplementedError, match="Subclasses must implement this method."
    ):
        client.create_collection(
            name="test_collection", vector_size=128, distance_metric="cosine"
        )


def test_base_dbclient_insert_vector():
    """
    Test that BaseDBClient.insert_vector() raises NotImplementedError.
    """
    client = DummyDBClient()
    with pytest.raises(
        NotImplementedError, match="Subclasses must implement this method."
    ):
        client.insert_vector(
            collection_name="test_collection",
            vector_id="vec1",
            vector=[0.1, 0.2, 0.3],
        )


def test_base_dbclient_search_vectors():
    """
    Test that BaseDBClient.search_vectors() raises NotImplementedError.
    """
    client = DummyDBClient()
    with pytest.raises(
        NotImplementedError, match="Subclasses must implement this method."
    ):
        client.search_vectors(
            collection_name="test_collection", query_vector=[0.1, 0.2, 0.3]
        )


def test_dbclient_initialization(db_client):
    """
    Test the initialization of the DBClient with a Qdrant backend.
    """
    assert isinstance(db_client._client, MagicMock)


def test_qdrant_connect(qdrant_client):
    """
    Test successful connection to the Qdrant server.
    """
    with patch.object(qdrant_client, "client", MagicMock()):
        qdrant_client.connect()
        qdrant_client.logger.info.assert_called_once_with(
            "Successfully connected to Qdrant at localhost:6333"
        )


def test_qdrant_connect_failure(qdrant_client):
    """
    Test connection failure handling in QdrantDBClient.
    """
    with patch(
        "darca_vector_db.db_client.QdrantClient",
        side_effect=Exception("Connection Failed"),
    ):
        with pytest.raises(DBConnectionError):
            qdrant_client.connect()

    # Check if the logger was called with the error message
    qdrant_client.logger.error.assert_called_once_with(
        "Connection to Qdrant failed", exc_info=True
    )


def test_create_collection_success(qdrant_client):
    """
    Test successful collection creation.
    """
    qdrant_client.client.create_collection.return_value = None
    qdrant_client.create_collection("test_collection", 128, "cosine")
    qdrant_client.logger.info.assert_called_once_with(
        "Collection 'test_collection' created successfully."
    )


def test_insert_vector_success(qdrant_client):
    """
    Test successful vector insertion.
    """
    qdrant_client.client.upsert.return_value = None
    qdrant_client.insert_vector("test_collection", "vec1", [0.1, 0.2, 0.3])
    qdrant_client.logger.info.assert_called_once_with(
        "Vector with ID 'vec1' inserted successfully into 'test_collection'."
    )


def test_insert_vector_failure(qdrant_client):
    """
    Test vector insertion failure handling.
    """
    qdrant_client.client.upsert.side_effect = Exception("Insertion Failed")

    with pytest.raises(VectorInsertionError):
        qdrant_client.insert_vector("test_collection", "vec1", [0.1, 0.2, 0.3])

    qdrant_client.logger.error.assert_called_once()


def test_search_vectors_success(qdrant_client):
    """
    Test successful vector search operation.
    """
    qdrant_client.client.search.return_value = ["result1", "result2"]
    results = qdrant_client.search_vectors("test_collection", [0.1, 0.2, 0.3])

    assert results == ["result1", "result2"]
    qdrant_client.logger.info.assert_called_once_with(
        "Search completed successfully in collection 'test_collection'."
    )


def test_search_vectors_failure(qdrant_client):
    """
    Test vector search failure handling.
    """
    qdrant_client.client.search.side_effect = Exception("Search Failed")

    with pytest.raises(VectorSearchError):
        qdrant_client.search_vectors("test_collection", [0.1, 0.2, 0.3])

    qdrant_client.logger.error.assert_called_once()


def test_dbclient_backend_error():
    """
    Test unsupported backend initialization in DBClient.
    """
    with pytest.raises(Exception):
        DBClient(backend="invalid_backend")


def test_create_collection_invalid_distance_metric(qdrant_client):
    """
    Test collection creation failure due to invalid distance metric.
    This will cover line 143 where a ValueError is raised due to
    AttributeError.
    """
    with pytest.raises(
        ValueError, match="Unsupported distance metric: INVALID_METRIC"
    ):
        qdrant_client.create_collection(
            "test_collection", 128, "INVALID_METRIC"
        )


def test_create_collection_unexpected_response(qdrant_client):
    """
    Test collection creation failure due to an UnexpectedResponse exception.
    This will cover lines 145 and 146 where logger.error is called
    and CollectionCreationError is raised.
    """
    # Mock the client to raise an UnexpectedResponse with required arguments
    qdrant_client.client.create_collection.side_effect = UnexpectedResponse(
        reason_phrase="Bad Request",
        content="Error occurred while creating collection",
        headers={"Content-Type": "application/json"},
        status_code=400,
    )

    with pytest.raises(
        CollectionCreationError, match="Failed to create collection"
    ):
        qdrant_client.create_collection("test_collection", 128, "cosine")

    # Ensure the logger.error call is made
    qdrant_client.logger.error.assert_called_once_with(
        "Failed to create collection", exc_info=True
    )


def test_dbclient_connect(db_client):
    """
    Test the connect() method of DBClient.
    Ensures that the connection is made and the logger.info() is called.
    """
    db_client._client.connect = MagicMock()

    db_client.connect()

    db_client._client.connect.assert_called_once()
    db_client.logger.info.assert_called_once_with(
        "Connected to the vector database."
    )


def test_dbclient_create_collection(db_client):
    """
    Test the create_collection() method of DBClient.
    Ensures that the collection creation is made and the logger.info()
    is called.
    """
    db_client._client.create_collection = MagicMock()

    db_client.create_collection("test_collection", 128, "cosine")

    db_client._client.create_collection.assert_called_once_with(
        "test_collection", 128, "cosine"
    )
    db_client.logger.info.assert_called_once_with(
        "Collection 'test_collection' created."
    )


def test_dbclient_insert_vector(db_client):
    """
    Test the insert_vector() method of DBClient.
    Ensures that the vector insertion is made and the logger.info()
    is called.
    """
    db_client._client.insert_vector = MagicMock()

    db_client.insert_vector("test_collection", "vec1", [0.1, 0.2, 0.3])

    db_client._client.insert_vector.assert_called_once_with(
        "test_collection", "vec1", [0.1, 0.2, 0.3], None
    )
    db_client.logger.info.assert_called_once_with(
        "Vector 'vec1' inserted into collection 'test_collection'."
    )


def test_dbclient_search_vectors(db_client):
    """
    Test the search_vectors() method of DBClient.
    Ensures that the search operation is made and the logger.info() is called.
    """
    db_client._client.search_vectors = MagicMock(
        return_value=["result1", "result2"]
    )

    results = db_client.search_vectors("test_collection", [0.1, 0.2, 0.3])

    db_client._client.search_vectors.assert_called_once_with(
        "test_collection", [0.1, 0.2, 0.3], 10
    )
    db_client.logger.info.assert_called_once_with(
        "Search completed in collection 'test_collection'."
    )
    assert results == ["result1", "result2"]


def test_dbclient_getattr(db_client):
    """
    Test the __getattr__() method of DBClient.
    Ensures that method calls are delegated to the backend client.
    """
    db_client._client.some_method = MagicMock(return_value="delegated")

    result = db_client.some_method()

    assert result == "delegated"
    db_client._client.some_method.assert_called_once()
