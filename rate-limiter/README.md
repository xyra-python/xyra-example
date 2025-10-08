## Rate Limiting Middleware

Xyra provides a built-in rate limiter middleware to limit requests per client:

```python
from xyra import App
from xyra.middleware import rate_limiter

app = App()

# Add rate limiter: 100 requests per minute per IP
app.use(rate_limiter(requests=100, window=60))

@app.get("/")
def home(req, res):
    res.json({"message": "Hello World"})
```

### Rate Limiter Options

```python
# 10 requests per second
app.use(rate_limiter(requests=10, window=1))

# 1000 requests per hour
app.use(rate_limiter(requests=1000, window=3600))

# Custom key function (by user ID instead of IP)
def get_user_key(req):
    return req.get_header("X-User-ID") or "anonymous"

app.use(rate_limiter(requests=50, window=60, key_func=get_user_key))
```

### Rate Limit Headers

The middleware adds standard rate limit headers:

- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Time when the limit resets (Unix timestamp)

### Rate Limit Response

When limit is exceeded, returns HTTP 429 with:

```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please try again later.",
  "retry_after": 60
}
```