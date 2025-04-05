Usage Guide
===========

This document explains in detail how to use the `darca-vector-db` library, including setup, configuration, and using the provided API to interact with vector databases.

Installation
------------
The recommended way to install `darca-vector-db` is via `Poetry`.

1. Clone the repository:
   .. code-block:: bash

       git clone https://github.com/roelkist/darca-vector-db.git
       cd darca-vector-db

2. Create a virtual environment and install dependencies:
   .. code-block:: bash

       make venv
       make poetry
       make install

Basic Usage
-----------
The `darca-vector-db` library provides a simple interface to interact with a vector database. The backend currently supported is `Qdrant`.

Importing the Library
---------------------
You can import the necessary components from the package as follows:

.. code-block:: python

    from darca_vector_db import DBClient, DBClientException, QdrantDBClient, BaseDBClient

Creating a Client
-----------------
To create a client for interacting with a Qdrant vector database:

.. code-block:: python

    client = DBClient(backend="qdrant", host="localhost", port=6333)
    client.connect()

The `DBClient` class acts as a unified interface for interacting with different vector databases.

Creating a Collection
---------------------
To create a collection in the Qdrant database, use the `create_collection` method:

.. code-block:: python

    client.create_collection(
        name="my_vectors",
        vector_size=128,
        distance_metric="cosine"
    )

Parameters:
- `name`: The name of the collection to create.
- `vector_size`: The size of the vectors to be stored in the collection.
- `distance_metric`: The distance metric to use for comparisons. Supported values: `cosine`, `euclidean`, `dot`.

Inserting Vectors
-----------------
To insert a vector into a collection:

.. code-block:: python

    client.insert_vector(
        collection_name="my_vectors",
        vector_id="1",
        vector=[0.1, 0.2, 0.3, ...],  # A vector of size 128
        metadata={"label": "example"}
    )

Parameters:
- `collection_name`: Name of the collection to insert the vector into.
- `vector_id`: Unique identifier for the vector.
- `vector`: The actual vector data (list of floats).
- `metadata`: Optional dictionary of metadata associated with the vector.

Searching for Vectors
---------------------
To search for similar vectors within a collection:

.. code-block:: python

    results = client.search_vectors(
        collection_name="my_vectors",
        query_vector=[0.1, 0.2, 0.3, ...],
        top_k=5
    )
    print(results)

Parameters:
- `collection_name`: Name of the collection to search within.
- `query_vector`: The vector to search for.
- `top_k`: The number of most similar vectors to return.

Error Handling
--------------
All errors related to vector database operations are raised as subclasses of `DBClientException`.

Example:

.. code-block:: python

    try:
        client.connect()
    except DBClientException as e:
        print(f"An error occurred: {e.message}")

Custom Exceptions Provided:
- `DBClientException`: Base exception for all vector database errors.
- `DBConnectionError`: Raised when the connection to the database fails.
- `CollectionCreationError`: Raised when collection creation fails.
- `VectorInsertionError`: Raised when vector insertion fails.
- `VectorSearchError`: Raised when vector searching fails.

