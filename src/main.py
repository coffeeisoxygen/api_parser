import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.lifespan_config import lifespan
from src.config.log_settings import initialize_logging
from src.config.server_settings import get_uvicorn_config, settings
from src.exceptions.exception_handlers import (
    RequestValidationError,
    global_exception_handler,
)
from src.router.router_handler import register_debug_routers
from src.router.transaction import router as transaction_router

initialize_logging()
app = FastAPI(lifespan=lifespan)


# Setup CORS
def parse_cors_list(val: str):
    if val == "*":
        return ["*"]
    return [v.strip() for v in val.split(",") if v.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=parse_cors_list(settings.cors_allow_origins),
    allow_credentials=bool(settings.cors_allow_credentials),
    allow_methods=parse_cors_list(settings.cors_allow_methods),
    allow_headers=parse_cors_list(settings.cors_allow_headers),
)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)


@app.get("/")
async def read_root():
    """Root endpoint for health check and welcome message."""
    return {"message": "Hello, World!"}


app.include_router(transaction_router)
register_debug_routers(app)

if __name__ == "__main__":
    config = get_uvicorn_config()
    uvicorn.run(
        app="src.main:app",
        host=str(config["host"]),
        port=int(config["port"]),
        reload=bool(config["reload"]),
    )
