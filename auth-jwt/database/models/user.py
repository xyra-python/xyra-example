# database/models/user.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from database.engine import Base
from config.security import get_password_hash, verify_password

class User(AsyncAttrs, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)

    @classmethod
    def create(cls, name: str, email: str, password: str):
        hashed_password = get_password_hash(password)
        return cls(name=name, email=email, hashed_password=hashed_password)