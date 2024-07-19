from litestar import Controller, HttpMethod, route


class HealthCheckController(Controller):
    path = "/health"
    security = None
    guards = []

    @route(
        http_method=HttpMethod.GET,
        path="/",
    )
    async def get_check(
        self,
    ) -> dict[str, str]:
        return {"status": "OK"}
