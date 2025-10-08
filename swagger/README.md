# Swagger Example with Xyra

This example demonstrates comprehensive Swagger (OpenAPI) integration in a Xyra application, including detailed API documentation, multiple endpoints, and custom configuration.

## Features

- **Automatic Documentation**: Swagger generates docs from route definitions and docstrings
- **Custom Configuration**: Title, version, contact info, servers, etc.
- **Complete CRUD API**: Full REST operations for items
- **Query Parameters**: Pagination support
- **Error Handling**: Proper HTTP status codes

## Setup

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## API Endpoints

- `GET /` - Root endpoint with API info
- `GET /items` - Get all items (with pagination)
- `GET /items/{item_id}` - Get item by ID
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item
- `GET /health` - Health check

## Documentation Access

- **Swagger UI**: `http://localhost:8000/docs`
- **JSON Specification**: `http://localhost:8000/docs/swagger.json`

## Swagger Configuration

The app is configured with:
- Custom title, version, and description
- Contact and license information
- Multiple server environments
- Custom paths for docs

All endpoints include detailed docstrings that are automatically included in the generated documentation.