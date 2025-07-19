import uvicorn
from fastapi import FastAPI

from src.config.lifespan_config import lifespan
from src.config.log_settings import initialize_logging
from src.config.server_settings import get_uvicorn_config
from src.exceptions.exception_handlers import (
    RequestValidationError,
    global_exception_handler,
)
from src.router.router_handler import register_debug_routers
from src.router.transaction import router as transaction_router

initialize_logging()
app = FastAPI(lifespan=lifespan)
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
