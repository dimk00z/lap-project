import structlog
from litestar import Controller, MediaType, Request, get
from litestar.response import Response

from src.app.domain.accounts.system.schemas import SystemHealth
from src.app.domain.accounts.system.urls import LIVENESS, SYSTEM_HEALTH

logger = structlog.get_logger()


class SystemController(Controller):
    tags = ["System"]

    @get(
        operation_id="SystemHealth",
        name="system:health",
        path=SYSTEM_HEALTH,
        media_type=MediaType.JSON,
        cache=False,
        tags=["System"],
        summary="Health Check",
        description="Execute a health check against backend.",
        exclude_from_auth=True,
    )
    async def check_system_health(
        self,
        request: Request,
    ) -> Response[SystemHealth]:
        await logger.adebug(
            "System Health check",
        )
        return Response(
            content=SystemHealth(),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @get(
        operation_id="SystemLivenessCheck",
        name="system:liveness_check",
        path=LIVENESS,
        media_type=MediaType.TEXT,
        cache=False,
        tags=["System"],
        summary="Liveness Check",
        description="Execute a health check against backend.",
        exclude_from_auth=True,
    )
    async def liveness_check(
        self,
        request: Request,
    ) -> Response[str]:
        """Liveness Check."""
        return Response(
            content="OK",
            status_code=200,
            media_type=MediaType.TEXT,
        )
