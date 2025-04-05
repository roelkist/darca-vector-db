Contributing to darca-vector-db
===============================

Thank you for considering contributing to darca-vector-db! Your contributions help make this project better.

Getting Started
---------------
To set up your local environment for development, follow these steps:

1. Clone the repository:
   .. code-block:: bash

       git clone https://github.com/roelkist/darca-vector-db.git
       cd darca-vector-db

2. Create a virtual environment and install dependencies:
   .. code-block:: bash

       make venv
       make poetry
       make install

3. Run the tests to ensure your setup is correct:
   .. code-block:: bash

       make test

Creating Pull Requests (PRs)
----------------------------
All contributions should be made by directly creating a new branch in the main repository (no forking is needed).

1. Create a new branch:
   .. code-block:: bash

       git checkout -b feature/my-awesome-feature

2. Make your changes, following the project’s coding standards and guidelines.

3. Run the complete check to ensure that your changes comply:
   .. code-block:: bash

       make check

4. Commit your changes with a descriptive message:
   .. code-block:: bash

       git commit -m "Add feature: My awesome feature"

5. Push your branch:
   .. code-block:: bash

       git push origin feature/my-awesome-feature

6. Open a Pull Request (PR) against the `main` branch.

Issues and Feature Requests
---------------------------
To report a bug or request a new feature, please open an issue on the GitHub repository:
`Issues on GitHub <https://github.com/roelkist/darca-vector-db/issues>`_

Before submitting, ensure that the issue or request does not already exist.

Guidelines
----------
- Make sure to run `make check` before committing changes.
- Use separate `make` targets (like `make test`, `make format`) instead of running everything at once.
- Include tests for new features or bug fixes.
- Write clear and concise commit messages.
- Keep your code consistent with existing code style.

Code of Conduct
---------------
We are committed to providing a welcoming and inclusive environment. Please be respectful and considerate in your interactions.

License
-------
By contributing, you agree that your contributions will be licensed under the MIT License.
