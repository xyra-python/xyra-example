from xyra import Request, Response
from database.engine import get_db
from handler.schemas import UserUpdate
from handler.crud import get_users, get_user, update_user, delete_user, get_user_by_email

def register_user_routes(app):
    @app.get("/users")
    async def read_users(req: Request, res: Response):
        db_gen = get_db()
        db = await db_gen.__anext__()
        try:
            users = await get_users(db)
            user_list = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
            res.json(user_list)
        except Exception as e:
            res.status(500).json({"error": str(e)})
        finally:
            await db.close()

    @app.get("/users/{user_id}")
    async def read_user(req: Request, res: Response):
        db_gen = get_db()
        db = await db_gen.__anext__()
        try:
            user_id = int(req.params.get("user_id"))
            db_user = await get_user(db, user_id)
            if not db_user:
                res.status(404).json({"error": "User not found"})
                return
            res.json({
                "id": db_user.id,
                "name": db_user.name,
                "email": db_user.email
            })
        except Exception as e:
            res.status(400).json({"error": str(e)})
        finally:
            await db.close()

    @app.put("/users/{user_id}")
    async def update_user_route(req: Request, res: Response):
        db_gen = get_db()
        db = await db_gen.__anext__()
        try:
            user_id = int(req.params.get("user_id"))
            user_data = await req.json()
            user_update = UserUpdate(**user_data)

            # Check if email is being updated and if it conflicts
            if user_update.email:
                existing = await get_user_by_email(db, user_update.email)
                if existing and existing.id != user_id:
                    res.status(400).json({"error": "Email already registered"})
                    return

            db_user = await update_user(db, user_id, user_update)
            if not db_user:
                res.status(404).json({"error": "User not found"})
                return
            res.json({
                "id": db_user.id,
                "name": db_user.name,
                "email": db_user.email,
                "message": "User updated successfully"
            })
        except Exception as e:
            res.status(400).json({"error": str(e)})
        finally:
            await db.close()

    @app.delete("/users/{user_id}")
    async def delete_user_route(req: Request, res: Response):
        db_gen = get_db()
        db = await db_gen.__anext__()
        try:
            user_id = int(req.params.get("user_id"))
            deleted = await delete_user(db, user_id)
            if deleted:
                res.json({"message": "User deleted successfully"})
            else:
                res.status(404).json({"error": "User not found"})
        except Exception as e:
            res.status(400).json({"error": str(e)})
        finally:
            await db.close()