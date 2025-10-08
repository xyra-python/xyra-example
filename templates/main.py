from xyra import App, Request, Response

app = App(
    templates_directory="templates"
)

@app.get("/")
def index(req: Request, res: Response):
    res.render("index.html", title="Home")

@app.get("/about")
def about(req: Request, res: Response):
    res.render("about.html", title="About")

if __name__ == "__main__":
    app.listen(8000)