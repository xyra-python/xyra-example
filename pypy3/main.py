# app.py
from xyra import App, Request, Response

app = App(
)

@app.get("/")
async def hello(req: Request, res: Response):
    return {"message": "Hello, Xyra!"}

@app.get("/users/{user_id}")
async def get_user(req: Request, res: Response):
    user_id = req.params.get("user_id")
    res.json({"user_id": user_id, "name": f"User {user_id}"})

if __name__ == "__main__":
    app.listen(8000)
