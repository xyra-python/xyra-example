from rate_limiter import app


def test_app_creation():
    assert app is not None


def test_routes():
    routes = app.router.routes
    assert len(routes) == 2
    route_paths = [route["parsed_path"] for route in routes]
    assert "/" in route_paths
    assert "/api" in route_paths


def test_middleware():
    assert len(app.middlewares) == 1
