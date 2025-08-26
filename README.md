# Financial API Test Automation Framework

This project is a Python-based test automation framework for the Alpha Vantage financial data API, built to demonstrate core SDET principles. It tests API endpoints for validity, data integrity, and error handling, and includes database integration for data persistence checks.

## Features

- **API Testing:** Uses `pytest` and `requests` to test the `/query` endpoint.
- **Data Validation:** Includes tests for successful responses, error conditions, and correct data types.
- **Database Integration:** Saves fetched data to an SQLite database and verifies data integrity.
- **Secure Key Management:** Uses `python-dotenv` to manage API keys securely.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/arup5biswas/Financial-API-Test-Automation-Framework.git
    cd Financial-API-Test-Automation-Framework
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your API key:**
    Create a `.env` file in the root directory and add your Alpha Vantage API key:
    `API_KEY=YOUR_API_KEY`

## How to Run Tests

To run the entire test suite, execute the following command from the root directory:
```bash
pytest -v
