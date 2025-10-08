# MySQL CRUD Example with Xyra

This is a simple CRUD application using Xyra framework and MySQL.

## Setup

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Set up your MySQL database and update `.env` with the correct DATABASE_URL.

3. Run the application:
   ```bash
   python main.py
   ```

## Endpoints

- `GET /users` - List all users
- `POST /users` - Create a new user (body: {"name": "string", "email": "string"})
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user (body: {"name": "string", "email": "string"})
- `DELETE /users/{user_id}` - Delete a user