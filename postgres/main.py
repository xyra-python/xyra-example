from xyra import App, Request, Response
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from typing import Optional
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname").replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

app = App()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_user_by_id(session, user_id: int):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user_in_db(session, name: str, email: str):
    user = User(name=name, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def update_user_in_db(session, user, name: Optional[str], email: Optional[str]):
    if name:
        user.name = name
    if email:
        user.email = email
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user_in_db(session, user):
    await session.delete(user)
    await session.commit()

@app.get("/users")
async def get_users(req: Request, res: Response):
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        res.json([{"id": u.id, "name": u.name, "email": u.email} for u in users])

@app.post("/users")
async def create_user(req: Request, res: Response):
    data = await req.json()
    async with async_session() as session:
        user = await create_user_in_db(session, data["name"], data["email"])
        res.json({"id": user.id, "name": user.name, "email": user.email})

@app.get("/users/{user_id}")
async def get_user(req: Request, res: Response):
    user_id = int(req.params.get("user_id"))
    async with async_session() as session:
        user = await get_user_by_id(session, user_id)
        if user:
            res.json({"id": user.id, "name": user.name, "email": user.email})
        else:
            res.status(404).json({"error": "User not found"})

@app.put("/users/{user_id}")
async def update_user(req: Request, res: Response):
    user_id = int(req.params.get("user_id"))
    data = await req.json()
    async with async_session() as session:
        user = await get_user_by_id(session, user_id)
        if user:
            updated_user = await update_user_in_db(session, user, data.get("name"), data.get("email"))
            res.json({"id": updated_user.id, "name": updated_user.name, "email": updated_user.email})
        else:
            res.status(404).json({"error": "User not found"})

@app.delete("/users/{user_id}")
async def delete_user(req: Request, res: Response):
    user_id = int(req.params.get("user_id"))
    async with async_session() as session:
        user = await get_user_by_id(session, user_id)
        if user:
            await delete_user_in_db(session, user)
            res.json({"message": "User deleted"})
        else:
            res.status(404).json({"error": "User not found"})

if __name__ == "__main__":
    asyncio.run(init_db())
    app.listen(8000)