import asyncio

from database.engine import init_db
from middleware.cors import cors_middleware
from middleware.jwt import jwt_middleware
from router.auth import register_auth_routes
from router.user import register_user_routes

from xyra import App

app = App(swagger_options={
    "title": "Indra"
})

# Apply middlewares
app.use(cors_middleware)
app.use(jwt_middleware)

# Register routes
register_auth_routes(app)
register_user_routes(app)

async def startup():
    await init_db()

if __name__ == "__main__":
    asyncio.run(startup())
    print("🚀 Starting server...")
    app.listen(8000, reload=True)
    print("📍 Server running on http://localhost:8000")
    print("📚 API docs: http://localhost:8000/docs")
