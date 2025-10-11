from xyra import App, Request, Response

# simple swagger
"""
app = App(swagger_options={
    "title": "Swagger Example API",
    "version": "1.0.0",
    "description": "A comprehensive API example with Swagger documentation",
})
"""
# advanced
app = App(swagger_options={
    "title": "Swagger Example API",
    "version": "1.0.0",
    "description": "A comprehensive API example with Swagger documentation",
    "contact": {
        "name": "API Support",
        "email": "support@example.com",
        "url": "https://example.com/support"
    },
    "license_info": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    "servers": [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server"
        }
    ],
    "swagger_ui_path": "/docs",
    "swagger_json_path": "/docs/swagger.json"
})

# Sample data
items = [
    {"id": 1, "name": "Item 1", "description": "First item", "price": 10.99},
    {"id": 2, "name": "Item 2", "description": "Second item", "price": 15.49}
]

@app.get("/")
async def root(req: Request, res: Response):
    """
    Root endpoint.

    Returns:
        dict: Welcome message and API info.
    """
    res.json({
        "message": "Welcome to Swagger Example API",
        "docs": "/docs",
        "version": "1.0.0"
    })

@app.get("/items")
async def get_items(req: Request, res: Response):
    """
    Get all items.

    Query Parameters:
        limit (int, optional): Maximum number of items to return. Default: 10
        offset (int, optional): Number of items to skip. Default: 0

    Returns:
        list: List of items.
    """
    limit = int(req.query_params.get("limit", ["10"])[0])
    offset = int(req.query_params.get("offset", ["0"])[0])
    paginated_items = items[offset:offset + limit]
    res.json(paginated_items)

@app.get("/items/{item_id}")
async def get_item(req: Request, res: Response):
    """
    Get item by ID.

    Path Parameters:
        item_id (int): The ID of the item to retrieve.

    Returns:
        dict: Item information.

    Raises:
        404: If item not found.
    """
    item_id = int(req.params.get("item_id"))
    item = next((i for i in items if i["id"] == item_id), None)
    if item:
        res.json(item)
    else:
        res.status(404).json({"error": "Item not found"})

@app.post("/items")
async def create_item(req: Request, res: Response):
    """
    Create a new item.

    Request Body:
        name (str): Item name
        description (str): Item description
        price (float): Item price

    Returns:
        dict: Created item.
    """
    data = await req.json()
    new_item = {
        "id": len(items) + 1,
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price")
    }
    items.append(new_item)
    res.status(201).json(new_item)


@app.put("/items/{item_id}")
async def update_item(req: Request, res: Response):
    """
    Update an existing item.

    Path Parameters:
        item_id (int): The ID of the item to update.

    Request Body:
        name (str, optional): Updated item name
        description (str, optional): Updated item description
        price (float, optional): Updated item price

    Returns:
        dict: Updated item.

    Raises:
        404: If item not found.
    """
    item_id = int(req.params.get("item_id"))
    data = await req.json()
    item = next((i for i in items if i["id"] == item_id), None)
    if item:
        item.update(data)
        res.json(item)
    else:
        res.status(404).json({"error": "Item not found"})

@app.delete("/items/{item_id}")
async def delete_item(req: Request, res: Response):
    """
    Delete an item.

    Path Parameters:
        item_id (int): The ID of the item to delete.

    Returns:
        dict: Success message.

    Raises:
        404: If item not found.
    """
    item_id = int(req.params.get("item_id"))
    global items
    items = [i for i in items if i["id"] != item_id]
    res.json({"message": "Item deleted"})

@app.get("/health")
async def health_check(req: Request, res: Response):
    """
    Health check endpoint.

    Returns:
        dict: Health status.
    """
    res.json({"status": "healthy", "timestamp": "2025-01-01T00:00:00Z"})

if __name__ == "__main__":
    app.listen(8000, logger=True, reload=True)
