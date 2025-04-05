darca-vector-db
===============

A pluggable vector database client system with backend support. Currently, the only supported backend is Qdrant.

This project provides a unified client interface to interact with vector databases. It is designed to be easily extensible to support additional backends in the future.

GitHub Repository:
------------------
Visit the official repository at: `darca-vector-db on GitHub <https://github.com/roelkist/darca-vector-db>`_

Installation
------------
The project uses `Poetry` for dependency management and virtual environment handling.

To set up the project locally, follow these steps:

1. Clone the repository:
   .. code-block:: bash

       git clone https://github.com/roelkist/darca-vector-db.git
       cd darca-vector-db

2. Create a virtual environment and install dependencies:
   .. code-block:: bash

       make venv
       make poetry
       make install

3. Running tests:
   .. code-block:: bash

       make test

4. Formatting the code:
   .. code-block:: bash

       make format

5. Building the documentation:
   .. code-block:: bash

       make docs

Features
--------
- Unified client interface for vector databases
- Qdrant support
- Easy to extend for additional backends
- Structured logging and error handling
- Flexible CI and local environment support
- Automated testing and code formatting

Usage
-----
To use the client, instantiate it with the desired backend (currently only Qdrant is supported):

.. code-block:: python

    from darca_vector_db import DBClient

    client = DBClient(backend="qdrant", host="localhost", port=6333)
    client.connect()
    client.create_collection(name="my_vectors", vector_size=128)
    client.insert_vector("my_vectors", vector_id="1", vector=[0.1, 0.2, 0.3])
    results = client.search_vectors("my_vectors", query_vector=[0.1, 0.2, 0.3])
    print(results)

Contributing
------------
Contributions are welcome! Please refer to the `CONTRIBUTING.rst` for detailed guidelines.

License
-------
MIT License

Author
------
Roel Kist
