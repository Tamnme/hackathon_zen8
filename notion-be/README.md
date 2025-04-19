# User API

A simple user management API with JSON file storage built with FastAPI.

## Features

- User registration and authentication
- JWT token-based authentication
- JSON file-based data persistence
- RESTful API endpoints
- Comprehensive unit tests

## Requirements

- Python 3.9+
- Packages listed in requirements.txt

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/user-api.git
   cd user-api
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Running the API

Run the API server:

```bash
source venv/bin/activate && python3 run.py
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the OpenAPI documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /token` - Login to get access token

### Users

- `GET /users` - Get all users (requires authentication)
- `GET /users/me` - Get current user (requires authentication)
- `GET /users/{user_id}` - Get a specific user (requires authentication)
- `POST /users` - Create a new user (public endpoint)
- `PUT /users/{user_id}` - Update a user (requires authentication)
- `DELETE /users/{user_id}` - Delete a user (requires authentication)

## Running Tests

Run all tests:

```bash
source venv/bin/activate && pytest app/tests
```

Run specific tests:

```bash
source venv/bin/activate && pytest app/tests/test_user_service.py -v
source venv/bin/activate && pytest app/tests/test_api_simple.py -v
``` 