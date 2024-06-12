from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse, JSONResponse

from config.log_config import setup_logging
from controller.auth_controller import auth_router
from controller.user_controller import user_router
from messaging.rabbitmq_consumer import consumer_thread

consumer_thread.start()

logger = setup_logging()

logger.info('Starting application')

app = FastAPI(
    title="Users API",
    description="API para gerenciamento de usuários",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=None,
    contact={
        "name": "Luan Fernandes",
        "email": "souluanf@icloud.com",
        "url": "https://luanfernandes.dev"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://users.luanfernandes.dev",
            "description": "Production server"
        }
    ],
)

app.include_router(auth_router)
app.include_router(user_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"}
    )


@app.get("/", tags=["Redirect"], include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/docs", tags=["Redirect"], include_in_schema=False)
async def get_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Swagger UI"
    )


@app.get("/openapi.json", tags=["Redirect"], include_in_schema=False)
async def get_openapi():
    return get_swagger_ui(
        title="Users API",
        version="1.0.0",
        description="API para gerenciamento de usuários",
        routes=app.routes,
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

# TODO: colocar comandos dokcer no README.md
