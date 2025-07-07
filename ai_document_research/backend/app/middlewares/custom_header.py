from fastapi import Request
from fastapi.responses import Response

# Middleware to add a custom header to all responses
async def add_custom_header(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-App-Version"] = "1.0.0"
    return response