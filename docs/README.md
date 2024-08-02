# PlatinumAI API Documentation

Welcome to the PlatinumAI API documentation. This guide will help you set up, configure, and use the API effectively. PlatinumAI API offers advanced features like auto-provider selection, MongoDB integration, and real-time streaming for AI interactions.

## Table of Contents

1. [Overview](#overview)
2. [Setup](#setup)
3. [Configuration](#configuration)
4. [API Endpoints](#api-endpoints)
   - [Root Endpoint](#root-endpoint)
   - [Chat Completions](#chat-completions)
   - [Available Models](#available-models)
5. [Usage](#usage)
6. [Rate Limiting](#rate-limiting)
7. [Error Handling](#error-handling)
8. [License](#license)

## Overview

PlatinumAI API provides a unified interface to interact with multiple AI providers. It supports automatic provider selection, user authentication via API keys, rate limiting, and detailed logging. The API is built using FastAPI and MongoDB.

## Setup

### Prerequisites

- Python 3.7+
- MongoDB Atlas account
- OpenAI API key

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/your-repo/platinumai-api.git
   cd platinumai-api
   ```

2. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Environment Variables**

   Set the following environment variables:

   - `MONGO_URI`: The connection URI for MongoDB.
   - `OPENAI_API_KEY`: Your OpenAI API key.

## Configuration

### MongoDB Setup

Ensure that your MongoDB instance is running and accessible. The API uses MongoDB for storing user data, request logs, and rate limit tracking.

### Enabling Intents

Make sure to enable the necessary intents for your application, as the API may require specific permissions to operate correctly.

## API Endpoints

### Root Endpoint

- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: Returns the static HTML content from the `/public` directory.

### Chat Completions

- **Endpoint**: `/v1/chat/completions`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: Bearer token for API key.
- **Body**:
  - `model`: The AI model to use (e.g., `gpt-3.5`).
  - `stream`: Optional boolean to indicate if streaming is required.
  - Other model-specific parameters.
- **Description**: Proxies the request to the selected AI provider and returns the response. Supports both streaming and non-streaming responses.

### Available Models

- **Endpoint**: `/v1/models`
- **Method**: `GET`
- **Description**: Returns a list of available AI models and their details.

## Usage

### Making Requests

To interact with the API, use the `/v1/chat/completions` endpoint. Include your API key in the `Authorization` header as a Bearer token. Specify the desired model and other parameters in the request body.

Example:

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "gpt-3.5",
  "messages": [{"role": "user", "content": "Hello, world!"}]
}'
```

## Rate Limiting

PlatinumAI API enforces rate limits based on the user's subscription plan:

- **Basic**: 15 requests per minute, 1000 requests per day
- **Pro**: 60 requests per minute, 5000 requests per day

Rate limits are reset daily at 13:00 Eastern Time.

## Error Handling

The API returns appropriate HTTP status codes and error messages for different failure scenarios. Common errors include:

- `400 Bad Request`: Invalid input or missing parameters.
- `401 Unauthorized`: Invalid or missing API key.
- `429 Too Many Requests`: Rate limit exceeded.

## License

This project is licensed under the Unlicense. For more information, see the [LICENSE](../LICENSE) file.
