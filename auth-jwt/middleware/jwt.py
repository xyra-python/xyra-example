from config.security import verify_token

from xyra import Request, Response


async def jwt_middleware(req: Request, res: Response, next_call):
    # Skip authentication for auth routes
    if req.url.startswith("/auth"):
        return await next_call(req, res)

    auth_header = req.get_header("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        res.status(401).json({"error": "Not authenticated"})
        return

    token = auth_header.split(" ")[1]
    try:
        email = await verify_token(token)
        # Store user email in request object for later use
        req.user_email = email
    except Exception:
        res.status(401).json({"error": "Invalid token"})
        return

    return await next_call(req, res)
