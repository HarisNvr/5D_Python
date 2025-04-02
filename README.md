# FastAPI URL Shortener

This is a simple URL shortener service built with FastAPI. It allows users to shorten URLs, retrieve the original URL using a short identifier, and perform asynchronous HTTP requests.

## Features

- Shorten a given URL
- Retrieve the original URL via a short identifier
- Perform an asynchronous HTTP request and return the response
- Uses Redis for storage
- Packaged with Docker and Docker Compose for easy deployment

## Installation and Setup

### 1. Clone the repository
```sh
git clone https://github.com/HarisNvr/5D_Python.git
cd 5D_Python
```

### 2. Install dependencies (Optional, for local development)
```sh
pip install -r requirements.txt
```

### 3. Run with Docker Compose
```sh
docker-compose up --build
```

This will start the FastAPI service and Redis in separate containers.

## API Endpoints

### 1. Shorten a URL
**POST /**
```sh
curl -X POST "http://127.0.0.1:8080/" -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
```
**Response:**
```json
{
  "short_url": "abcd1234"
}
```

### 2. Retrieve the original URL
**GET /{short_id}**
```sh
curl -L "http://127.0.0.1:8080/abcd1234"
```
Redirects to the original URL.

### 3. Fetch data from a URL
**GET /fetch?url=<URL>**
```sh
curl "http://127.0.0.1:8080/fetch?url=https://jsonplaceholder.typicode.com/todos/1"
```
**Response:**
```json
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

### 4. Print Redis storage (for debugging purposes)
**GET /storage**
```sh
curl "http://127.0.0.1:8080/storage"
```
**Response:**
```json
{
    "452019f8": "https://example.com/",
    "939c36a2": "https://ya.ru/"
}
```

## Environment Variables
- `REDIS_URL` - Redis connection URL (default: `redis://redis:6379`)