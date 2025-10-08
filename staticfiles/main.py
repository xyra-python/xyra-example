from xyra import App, Request, Response

app = App(templates_directory="templates")

# Serve static files from 'static' directory
app.static_files("/static", "static")

# Add helper function for static files in templates
# app.templates.add_global("static", lambda path: f"/static/{path}")

@app.get("/")
def index(req: Request, res: Response):
    res.render("index.html", title="Static Files Example")

if __name__ == "__main__":
    app.listen(8000)