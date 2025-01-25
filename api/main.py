import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_swagger_ui_html
)
from fastapi.responses import JSONResponse

from app.main import setup_bot


def register_exception(application):
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        # or logger.error(f'{exc}')
        print(request, exc_str)
        content = {'status_code': 422, 'message': exc_str, 'data': None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


def register_cors(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@asynccontextmanager
async def application_lifespan(app: FastAPI):
    bot_events = setup_bot(app)
    if bot_events is not None:
        on_startup, on_shutdown = bot_events
    else:
        yield
        return

    if asyncio.iscoroutinefunction(on_startup):
        await on_startup()
    else:
        on_startup()
    yield
    if asyncio.iscoroutinefunction(on_shutdown):
        await on_shutdown()
    else:
        on_shutdown()


def init_web_application():
    application = FastAPI(
        openapi_url='/api/openapi.json',
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        lifespan=application_lifespan,
    )

    register_exception(application)
    register_cors(application)

    from api.routes.mailing import router as mailing_router
    from api.routes.admin import router as admin_router

    application.include_router(mailing_router)
    application.include_router(admin_router)

    @application.get("/api/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=application.title + " - Swagger UI",
            oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@latest/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@latest/swagger-ui.css",
        )

    return application


fastapi_app = init_web_application()
