from litestar.openapi import OpenAPIConfig
from litestar import Litestar
from piccolo.engine import engine_finder
from app.controllers.user import UserController
from litestar.openapi.plugins import SwaggerRenderPlugin, StoplightRenderPlugin

# Piccolo connection management
async def on_startup():
    engine = engine_finder()
    if engine:
        await engine.start_connection_pool()

async def on_shutdown():
    engine = engine_finder()
    if engine:
        await engine.close_connection_pool()


from app.middleware.auth import JWTAuthenticationMiddleware

api_config = OpenAPIConfig(
    title="Reddit Clone API",
    version="0.1.0",
    render_plugins=[SwaggerRenderPlugin()],
)

app = Litestar(
    route_handlers=[UserController],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    debug=True,
    openapi_config=api_config,
    middleware=[JWTAuthenticationMiddleware],
)