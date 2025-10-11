from xyra import App
from xyra.middleware import rate_limiter

app = App()

# Rate limit: 100 requests per minute per IP
app.use(rate_limiter(requests=10, window=60))

@app.get("/")
def get_data(req, res):
    res.json({"message": "Hello Wolrd"})

@app.get("/api")
def data(req, res):
    res.json({"data": "some data"})

if __name__ == "__main__":
    app.listen(8000, logger=True, reload=True)
