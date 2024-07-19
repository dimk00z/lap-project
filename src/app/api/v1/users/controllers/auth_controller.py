from litestar import Controller, get
from litestar.di import Provide

from server.api.v1.users.repository import UserRepository, provide_users_repo


class AuthController(Controller):
    path = "/"
    dependencies = {
        "users_repo": Provide(provide_users_repo),
        # "jwt_auth": Provide(JWTAuth[User]),
    }

    # @post(
    #     path="/",
    # )
    # async def login(
    #     self,
    #     # data: str,
    #     # jwt_auth: JWTAuth[User],
    # ) -> str:
    #     return "111"

    # #     print(data, jwt_auth)
    # #     return jwt_auth.login(
    # #         identifier=str(data.id),
    # #         token_extras={"email": data.email},
    # #         response_body=data,
    # #     )
    @get(
        path="/count",
    )
    async def get_users_count(
        self,
        users_repo: UserRepository,
    ) -> int:
        """Get users count."""
        return await users_repo.count()
