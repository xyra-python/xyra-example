# app.py
from xyra import App

app = App(
)

@app.get("/")
def hello(req, res):
    res.json({"message": "Hello, Xyra!"})

@app.get("/users/{user_id}")
def get_user(req, res):
    user_id = req.params.get("user_id")
    res.json({"user_id": user_id, "name": f"User {user_id}"})

if __name__ == "__main__":
    app.listen(8000, reload=True)
