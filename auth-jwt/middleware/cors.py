from xyra import Request, Response

async def cors_middleware(req: Request, res: Response, next_call):
    res.header("Access-Control-Allow-Origin", "*")
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    if req.method == "OPTIONS":
        res.status(200).send("")
        return

    return await next_call(req, res)