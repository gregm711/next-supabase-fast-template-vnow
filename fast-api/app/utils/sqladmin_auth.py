import os
import jwt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request


JWT_SECRET_KEY = os.environ["ADMIN_SECRET_KEY"]
JWT_ALGORITHM = "HS256"


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if (
            username == os.environ["ADMIN_USERNAME"]
            and password == os.environ["ADMIN_PASSWORD"]
        ):
            token = jwt.encode(
                {"sub": username},
                JWT_SECRET_KEY,
                algorithm=JWT_ALGORITHM,
            )

            request.session.update({"token": token})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        try:
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return True
        except jwt.InvalidTokenError:
            return False
