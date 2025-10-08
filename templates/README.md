# Templates and Swagger Example with Xyra

This example demonstrates how to use Jinja2 templates and Swagger API documentation in a Xyra application.

## Features

- **Templates**: Render dynamic HTML pages using Jinja2
- **Swagger**: Automatic API documentation generation
- **CRUD Operations**: Basic user management with in-memory storage

## Setup

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Usage

- **Home Page**: `http://localhost:8000/` - Renders a template with user list
- **API Endpoints**:
  - `GET /users` - Get all users (JSON)
  - `GET /users/{user_id}` - Get user by ID
  - `POST /users` - Create new user
- **Swagger Docs**: `http://localhost:8000/docs` - Interactive API documentation

## Files

- `main.py`: Application with routes, templates, and Swagger config
- `templates/home.html`: Jinja2 template for the home page