import uvicorn
from fastapi import FastAPI

from guard import SecurityMiddleware
from src.config.app_config import settings
from src.config.lifespan_config import lifespan
from src.config.log_settings import initialize_logging
from src.config.server_settings import get_uvicorn_config
from src.exceptions.exception_handlers import global_exception_handler
from src.guard.sec_config import get_guard_decorator, get_security_config
from src.router.transaction import router as transaction_router

initialize_logging()
app = FastAPI(lifespan=lifespan)
config = get_security_config()
guard_deco = get_guard_decorator(config)
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/")
@guard_deco.require_ip(whitelist=["192.168.1.0/24", "127.0.0.1/24", "10.2.0.1"])
async def read_root():
    """Root endpoint for health check and welcome message."""
    return {"message": "Hello, World!"}


app.include_router(transaction_router)


# Add global middleware
if settings.app_mode != "development":
    app.add_middleware(SecurityMiddleware, config=config)
else:
    # Bisa log info bahwa guard tidak diaktifkan
    print("FastAPI Guard tidak aktif di mode development")

# Required: Set decorator handler on app state
app.state.guard_decorator = guard_deco

if __name__ == "__main__":
    config = get_uvicorn_config()
    uvicorn.run(
        app="src.main:app",
        host=str(config["host"]),
        port=int(config["port"]),
        reload=bool(config["reload"]),
    )
