from litestar import Controller, HttpMethod, route


class SocialAppController(Controller):
    path = "/api/v1/social"

    @route(http_method=HttpMethod.GET, path="/test")
    async def get_test(
        self,
    ) -> str:
        return "Hello, world!"


class HealthCheckController(Controller):
    path = "/api/v1/health"

    @route(http_method=HttpMethod.GET, path="/")
    async def get_check(
        self,
    ) -> dict[str, str]:
        return {"status": "OK"}


HTTP_CONTROLLERS = [
    SocialAppController,
    HealthCheckController,
]
