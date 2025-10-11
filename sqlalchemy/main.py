"""
CRUD API with Xyra, SQLAlchemy, and Pydantic (similar to FastAPI)
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

from xyra import App, Request, Response
from xyra.exceptions import HTTPException
# Database setup
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}  # For Pydantic V2

    id: int
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables
Base.metadata.create_all(bind=engine)

# App
app = App(
    swagger_options={
        "title": "CRUD API with Xyra",
        "version": "1.0.0",
        "description": "FastAPI-like CRUD with Xyra, SQLAlchemy, and Pydantic",
    }
)


# Routes
@app.post("/users/")
async def create_user(req: Request, res: Response):
    """
    Create a new user.
    """
    try:
        user_data = await req.json()
        user = UserCreate(**user_data)  # Pydantic validation
    except Exception as e:
        raise HTTPException(422, f"Validation error: {str(e)}")

    db = next(get_db())
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        response_data = UserResponse.model_validate(db_user.__dict__)
        res.status(201).json(response_data.dict())
    except Exception as e:
        db.rollback()
        if "UNIQUE constraint" in str(e):
            raise HTTPException(400, "Email already registered")
        raise HTTPException(500, f"Database error: {str(e)}")


@app.get("/users/")
async def read_users(req: Request, res: Response):
    """
    Get all users.
    """
    db = next(get_db())
    users = db.query(User).all()
    response_data = [
        UserResponse.model_validate(user.__dict__).model_dump() for user in users
    ]
    res.json(response_data)


@app.get("/users/{user_id}")
async def read_user(req: Request, res: Response):
    """
    Get user by ID.
    """
    user_id_str = req.params.get("user_id")
    if not user_id_str:
        raise HTTPException(400, "Invalid user ID")

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(400, "User ID must be integer")

    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    response_data = UserResponse.model_validate(user.__dict__)
    res.json(response_data.model_dump())


@app.put("/users/{user_id}")
async def update_user(req: Request, res: Response):
    """
    Update user by ID.
    """
    user_id_str = req.params.get("user_id")
    if not user_id_str:
        raise HTTPException(400, "Invalid user ID")

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(400, "User ID must be integer")

    try:
        user_data = await req.json()
        user_update = UserCreate(**user_data)  # Pydantic validation
    except Exception as e:
        raise HTTPException(422, f"Validation error: {str(e)}")

    db = next(get_db())
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, "User not found")

    db_user.name = user_update.name
    db_user.email = user_update.email
    try:
        db.commit()
        db.refresh(db_user)
        response_data = UserResponse.model_validate(db_user.__dict__)
        res.json(response_data.dict())
    except Exception as e:
        db.rollback()
        if "UNIQUE constraint" in str(e):
            raise HTTPException(400, "Email already registered")
        raise HTTPException(500, f"Database error: {str(e)}")


@app.delete("/users/{user_id}")
async def delete_user(req: Request, res: Response):
    """
    Delete user by ID.
    """
    user_id_str = req.params.get("user_id")
    if not user_id_str:
        raise HTTPException(400, "Invalid user ID")

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(400, "User ID must be integer")

    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    db.delete(user)
    db.commit()
    res.json({"message": "User deleted successfully"})


if __name__ == "__main__":
    app.listen(8000, reload=True, logger=True)
