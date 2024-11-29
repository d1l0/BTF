# Beta Testing Framework (BTF) for Container Orchestration API

This repository is a **Beta Testing Framework (BTF)** designed to test APIs for container orchestration. It includes tools for testing the API locally or via CI/CD pipelines and provides OpenAPI documentation for easy API exploration.

---

## Features

- Comprehensive API testing framework for container orchestration.
- Supports local and CI/CD-based test execution.
- OpenAPI documentation with a "Try it out" feature.

---

## Requirements

- Python 3.x
- Virtual environment (`venv`)
- `pip` for package management

---

## Installation and Setup (Local Machine)

1. **Clone the repository**:

    ```bash
    git clone <repo_url>
    cd <repo_name>
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python3 -m venv ./venv
    . ./venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

---

## Running Tests

1. **Run test cases locally**:

    Use `pytest` for executing the test cases locally:

    ```bash
    pytest -vvv
    ```

2. **Run tests via GitHub Actions**:

    - Navigate to the **GitHub Actions** tab in repository.
    - Trigger the **CI/CD workflow** to execute the test cases remotely.

---

## CI/CD Pipeline

The repository includes a pre-configured GitHub Actions workflow for:

- Running the test suite.
- Automated code checks and deployments.

---

## How to View OpenAPI Documentation

1. **Run the application**:

    Start the Flask server to serve the OpenAPI documentation:

    ```bash
    python3 tools/openapi.py --port=<desired_port>
    ```

    Replace `<desired_port>` with the port you want the application to run on (default: 5000).

2. **Access the documentation**:

    - Open your browser and navigate to `http://<host>:<desired_port>`.
    - Example: `http://localhost:5000`.

---

