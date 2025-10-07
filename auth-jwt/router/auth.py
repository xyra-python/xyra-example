from xyra import Request, Response
from database.engine import get_db
from handler.schemas import UserCreate, UserLogin
from handler.crud import create_user, get_user_by_email
from config.security import create_access_token

def register_auth_routes(app):
    @app.post("/auth/register")
    async def register(req: Request, res: Response):
        db_gen = get_db()
        db = await db_gen.__anext__()
        try:
            user_data = await req.json()
            user = UserCreate(**user_data)
            db_user = await get_user_by_email(db, user.email)
            if db_user:
                res.status(400).json({"error": "Email already registered"})
                return
            new_user = await create_user(db, user)
            res.status(201).json({
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "message": "User created successfully"
            })
        except Exception as e:
            res.status(400).json({"error": str(e)})
        finally:
            await db.close()

    @app.post("/auth/login")
    async def login(req: Request, res: Response):
        db_gen = get_db()
        db = await db_gen.__anext__()
        try:
            user_data = await req.json()
            user = UserLogin(**user_data)  # Use UserLogin instead of UserCreate
            db_user = await get_user_by_email(db, user.email)
            if not db_user or not db_user.verify_password(user.password):
                res.status(401).json({"error": "Incorrect email or password"})
                return
            access_token = create_access_token(data={"sub": user.email})
            res.json({"access_token": access_token, "token_type": "bearer"})
        except Exception as e:
            res.status(400).json({"error": str(e)})
        finally:
            await db.close()