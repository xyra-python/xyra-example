import pytest

try:
    from main import app
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False


@pytest.mark.skipif(not HAS_DEPENDENCIES, reason="Missing dependencies")
def test_app_creation():
    assert app is not None


@pytest.mark.skipif(not HAS_DEPENDENCIES, reason="Missing dependencies")
def test_routes():
    routes = app.router.routes
    assert len(routes) > 0
