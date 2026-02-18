# AI Expert Assignment 3

This repository contains a simple HTTP client and OAuth2 token management system.

## Project Structure
- `app/`: Application code
  - `http_client.py`: The HTTP client implementation
  - `tokens.py`: OAuth2 token handling
- `tests/`: Pytest suite

## Requirements
- Python 3.11+
- Pip (for local testing)
- Docker (for containerized testing)

## How to run tests locally

1.  **Clone the repository.**
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run pytest:**
    ```bash
    pytest -v
    ```

## How to build and run tests with Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t ai-expert-test .
    ```
2.  **Run the container:**
    ```bash
    docker run --rm ai-expert-test
    ```
    This will execute `pytest -v` inside the container by default.
