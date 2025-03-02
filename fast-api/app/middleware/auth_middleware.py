from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
import os
import jwt


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Example how to bypass auth for a specific endpoint and preflight requests
        if (
            request.url.path.startswith("/unprotected") or request.url.path.startswith("/favicon.ico")
            or request.method == "OPTIONS"
        ):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Missing or invalid authorization header"
            )

        # Extract the token from the header.
        token = auth_header.split(" ")[1]

        try:
            # Decode and verify the JWT token.
            # Replace 'JWT_SECRET' with your Supabase JWT secret if different.
            decoded_token = jwt.decode(
                token,
                os.environ["JWT_SECRET"],
                algorithms=["HS256"],
                audience="authenticated",  # Adjust audience as needed.
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Attach the decoded token payload to the request for downstream usage.
        request.state.user = decoded_token

        return await call_next(request)
