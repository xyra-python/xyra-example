# Static Files Example with Xyra

This is a simple example of serving static files and using templates with the Xyra framework.

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

- Visit `http://localhost:8000/` to see the main page rendered from template.
- Static files are served from `/static/` path, e.g., `http://localhost:8000/static/style.css`.

## Files

- `templates/index.html`: Jinja2 template for the main page
- `static/style.css`: CSS stylesheet