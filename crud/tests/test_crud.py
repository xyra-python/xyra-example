from main import app


def test_app_creation():
    assert app is not None


def test_routes():
    routes = app.router.routes
    assert len(routes) == 5  # get, post, get {id}, put {id}, delete {id}
    route_paths = [route["parsed_path"] for route in routes]
    assert "/users/" in route_paths
    assert "/users/{user_id}" in route_paths
