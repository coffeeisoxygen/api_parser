import uvicorn
from fastapi import FastAPI
from guard import SecurityDecorator, SecurityMiddleware

from src.config.app_config import settings
from src.config.lifespan_settings import lifespan
from src.config.log_settings import initialize_logging
from src.config.reg_exceptions import register_exception_handlers
from src.config.security_settings import SecurityConfig
from src.config.server_settings import get_uvicorn_config
from src.exceptions.exception_handlers import global_exception_handler
from src.router.transaction import router as transaction_router

# Initialize logging configuration
initialize_logging()
app = FastAPI(lifespan=lifespan)
config = SecurityConfig()
app.add_exception_handler(Exception, global_exception_handler)
# Create decorator instance
guard_deco = SecurityDecorator(config)


@app.get("/")
@guard_deco.require_ip(whitelist=["192.168.1.0/24", "127.0.0.1/24"])
async def read_root():
    """Root endpoint for health check and welcome message."""
    return {"message": "Hello, World!"}


app.include_router(transaction_router)

# Register exception handlers
register_exception_handlers(app)

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
