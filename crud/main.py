import asyncio
from logging import Logger
import aiosqlite
from xyra import App, Request, Response
from sqlite3 import IntegrityError


DB_PATH = "./users.db"

app = App()

async def create_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        await db.commit()
        print("Database initialized!")

@app.post("/users/")
async def create_user(req: Request, res: Response):
    try:
        user_data = await req.json()
        name = user_data.get("name")
        email = user_data.get("email")
        if not name or not email:
            return res.status(400).json({"error": "Name and email are required"})

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            await db.commit()

            cur = await db.execute("SELECT last_insert_rowid()")
            row = await cur.fetchone()
            user_id = row[0]

        return res.status(201).json({"id": user_id, "name": name, "email": email})
    except IntegrityError:
        return res.status(400).json({"error": "Email already registered"})
    except Exception as e:
        return res.status(500).json({"error": str(e)})

@app.get("/users/")
async def read_users(req: Request, res: Response):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT id, name, email FROM users")
        rows = await cur.fetchall()
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
    return res.json(users)

@app.get("/users/{user_id}")
async def read_user(req: Request, res: Response):
    user_id = req.params.get("user_id")
    if not user_id:
        return res.status(400).json({"error": "Invalid user ID"})

    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (int(user_id),)
        )
        row = await cur.fetchone()
        if not row:
            return res.status(404).json({"error": "User not found"})

        user = {"id": row[0], "name": row[1], "email": row[2]}
        return res.json(user)

@app.put("/users/{user_id}")
async def update_user(req: Request, res: Response):
    user_id = req.params.get("user_id")
    if not user_id:
        return res.status(400).json({"error": "Invalid user ID"})

    try:
        user_data = await req.json()
        name = user_data.get("name")
        email = user_data.get("email")
        if not name or not email:
            return res.status(400).json({"error": "Name and email are required"})

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (name, email, int(user_id))
            )
            await db.commit()

            cur = await db.execute("SELECT id, name, email FROM users WHERE id = ?", (int(user_id),))
            row = await cur.fetchone()
            if not row:
                return res.status(404).json({"error": "User not found"})

        updated_user = {"id": row[0], "name": row[1], "email": row[2]}
        return res.json(updated_user)
    except IntegrityError:
        return res.status(400).json({"error": "Email already registered"})
    except Exception as e:
        return res.status(500).json({"error": str(e)})

@app.delete("/users/{user_id}")
async def delete_user(req: Request, res: Response):
    user_id = req.params.get("user_id")
    if not user_id:
        return res.status(400).json({"error": "Invalid user ID"})

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM users WHERE id = ?", (int(user_id),))
        await db.commit()

        cur = await db.execute("SELECT id FROM users WHERE id = ?", (int(user_id),))
        row = await cur.fetchone()
        if not row:
            return res.status(404).json({"error": "User not found"})

    return res.json({"message": "User deleted successfully"})

if __name__ == "__main__":
    asyncio.run(create_db())
    app.listen(8080, reload=True)