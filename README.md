# 0xNeural BPE Tokenizer Engine

This project implements a FastAPI application that provides a custom-built Byte Pair Encoding (BPE) tokenizer specifically designed for Web3 source code. It addresses the "Context Window Crisis" in AI models analyzing smart contracts by providing an efficient, domain-specific text compression layer. Unlike standard tokenizers trained on general text, this engine is optimized for Solidity and other blockchain-specific syntax, ensuring that critical contextual information is preserved and AI models can process Web3 code effectively and rapidly.

## Motivation: The Context Window Crisis in Web3 Security

Web3 security demands real-time analysis of smart contracts, often before transactions are finalized. Traditional tokenization methods, whether character-level or word-level, fail in this specialized domain:

-   **Character-Level Tokenization**: Leads to extremely long sequences for common Web3 terms (e.g., "Ethereum" as eight tokens), rapidly exhausting AI model context windows and increasing API costs.
-   **Word-Level Tokenization**: Creates massive vocabularies prone to failure with typos or unseen hexadecimal addresses, breaking automated analysis pipelines.

Standard tokenizers, like OpenAI's `tiktoken`, are trained on general internet text (e.g., Wikipedia) and are "blind" to the architectural realities of Web3. They break down crucial syntax like `msg.sender` or `uint256` into scattered, meaningless shards, destroying the mathematical relationships between variables. This inefficiency is unacceptable in an industry where milliseconds can dictate millions in lost funds.

This project tackles this problem head-on by building a BPE tokenizer entirely from scratch in pure Python, bypassing generic frameworks to create a solution natively aware of Web3 syntax.

## Features

-   **Domain-Specific BPE Tokenization**: Implements a custom Byte Pair Encoding algorithm, trained on 9.8 million characters of deployed smart contracts, to efficiently tokenize Solidity and Web3-specific syntax. This ensures optimal compression and context preservation for AI models.
-   **FastAPI Backend**: A robust and high-performance web API built with FastAPI, enabling easy integration with other applications (e.g., real-time Ethereum mempool monitoring).
-   **Configurable Merge Rules**: Loads pre-trained merge rules from `web3_tokenizer_2000_merges.json`, allowing for flexible and specialized tokenization strategies.
-   **CORS Enabled**: Configured to allow cross-origin requests, facilitating seamless communication with various frontends (e.g., Streamlit applications).
-   **Health Check Endpoint**: Includes a `/` endpoint to verify the API's operational status.
-   **Encode Endpoint**: Provides an `/api/v1/encode` endpoint to tokenize source code, returning compressed token IDs.

## Benchmarks

The custom 2000-merge model demonstrates significant compression improvements, effectively tripling the context window for AI models analyzing smart contracts:

| Model       | Test Case                 | Original Bytes | Token Count | Compression Ratio |
| :---------- | :------------------------ | :------------- | :---------- | :---------------- |
| 2000_merges | Simple Transfer Function  | 54             | 11          | 5.61X             |
| 2000_merges | Complex DeFi Staking Contract | 1426           | 490         | 5.92X             |
| 2000_merges | Out-of-Distribution NFT Contract | -              | -           | 2.85X             |

These results highlight the effectiveness of training a domain-specific BPE tokenizer for improved compression and representation of specialized codebases, crucial for building robust Web3 security architectures.

## Technology Stack

-   **Python**: The core programming language.
-   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
-   **Uvicorn**: An ASGI server for running FastAPI applications.
-   **Pydantic**: Used for data validation and settings management.

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd 0xneural-Tokenizer
    ```
    (Replace `<repository_url>` with the actual URL of your repository.)

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate # On macOS/Linux
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the API

To start the FastAPI application, run the following command from the project root:

```bash
uvicorn tokenizer_api:app --host 0.0.0.0 --port 8000 --reload
```

-   `tokenizer_api:app`: Refers to the `app` object inside `tokenizer_api.py`.
-   `--host 0.0.0.0`: Makes the server accessible from all network interfaces.
-   `--port 8000`: Specifies the port to run the server on.
-   `--reload`: Enables auto-reloading on code changes (useful for development).

Once the server is running, you can access the API documentation at `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc).

### API Endpoints

#### Health Check

-   **GET /**
    -   **Description**: Checks if the API is live and listening.
    -   **Response**:
        ```json
        {
            "status": "Tokenizer API is live and listening."
        }
        ```

#### Encode Source Code

-   **POST /api/v1/encode**
    -   **Description**: Tokenizes the provided source code using the BPE algorithm.
    -   **Request Body**:
        ```json
        {
            "source_code": "function example() { return 1; }"
        }
        ```
    -   **Response**:
        ```json
        {
            "status": "success",
            "original_bytes": 30,
            "token_count": 10,
            "tokens": [256, 257, 10, 11, 12, 13, 14, 15, 16, 17]
        }
        ```
        (Note: `tokens` array will contain integer IDs representing the tokenized output.)

## Project Structure

-   `tokenizer_api.py`: Contains the FastAPI application, BPE tokenizer logic, and API endpoints.
-   `requirements.txt`: Lists the Python dependencies required for the project.
-   `web3_tokenizer_2000_merges.json`: A JSON file containing the pre-trained merge rules for the BPE tokenizer.

## Error Handling

-   **Empty Source Code**: If an empty `source_code` is provided to the `/api/v1/encode` endpoint, the API will return a `400 Bad Request` error.
-   **Weight Loading Error**: The application will print a fatal error message if it fails to load the `web3_tokenizer_2000_merges.json` file. Ensure this file is present and correctly formatted in the same directory as `tokenizer_api.py`.
