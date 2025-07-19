# Text Summarization API

A FastAPI-based web service for abstractive text summarization using a pretrained transformer model (ex. [DistilBART CNN-12-6](https://huggingface.co/sshleifer/distilbart-cnn-12-6)). This API receives articles and returns their summarized content.

## Features

- REST API for summarizing articles
- Batch summarization support
- Custom error handling for validation and empty input
- Docker support for easy deployment

## Requirements

- Python 3.8+
- pip

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/ByUnal/text-summarization.git
   cd text-summarization
   ```

2. **Install Dependencies:**
    ```sh
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    ```

## Running the API

**Locally**
```sh 
uvicorn main:app --reload --port 9073
```

With **Docker Build** and run the **Docker container**:
```sh 
docker build -t text-summarization .
docker run -p 9073:9073 text-summarization
```

## API Endpoints

### `GET /health`

Check the health status of the API.

**Response:**
```json
{
  "health_check": "OK",
  "httpStatus": 200
}
```
- `200 OK`: Returns the health status.

### `POST /summarize`

Summarize the given text.

#### Request Body

- `texts`: A single text or a list of texts to be summarized. (string or array of strings, required)
```json
{
  "texts": [
    "The quick brown fox jumps over the lazy dog.",
    "FastAPI is a modern web framework for Python that allows you to build APIs quickly with automatic interactive documentation."
  ]
}
```

#### Responses

- `200 OK`: Returns the summarized text(s).
- `400 BAD REQUEST`: Returns an error message if the input is empty or invalid.
```json
{
  "summaries": [
    "The quick brown fox jumps over the lazy dog.",
    "FastAPI is a modern web framework for Python that allows building APIs quickly."
  ]
}
```

### Error Response Example

```json
{
  "exceptionDetail": {
    "errorCode": "OSSB_AI_SUMMARIZATION_EXCEPTION",
    "errorMessage": "Fields cannot be empty",
    "service": "OSSB_AI_SUMMARIZATION_SERVICE"
  },
  "httpStatus": "BAD_REQUEST"
}
```

## License
This project is licensed under the Apache 2.0 License.
