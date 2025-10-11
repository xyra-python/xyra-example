from main import app


def test_app_creation():
    assert app is not None


def test_routes():
    routes = app.router.routes
    assert len(routes) == 1
    route_paths = [route["parsed_path"] for route in routes]
    assert "/health" in route_paths
