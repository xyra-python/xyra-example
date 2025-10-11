from main import app


def test_app_creation():
    assert app is not None


def test_routes():
    routes = app.router.routes
    assert len(routes) == 6  # root, items, items/{id}, etc.
    route_paths = [route["parsed_path"] for route in routes]
    assert "/" in route_paths
    assert "/items" in route_paths
    assert "/items/{item_id}" in route_paths
    assert "/health" in route_paths
