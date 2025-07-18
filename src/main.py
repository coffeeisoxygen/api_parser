import uvicorn
from fastapi import FastAPI
from guard import SecurityDecorator, SecurityMiddleware

from src.config.log_settings import initialize_logging
from src.config.security_settings import SecurityConfig
from src.config.server_settings import get_uvicorn_config
from src.router.transaction import router as transaction_router

# Initialize logging configuration
initialize_logging()
app = FastAPI()
config = SecurityConfig()

# Create decorator instance
guard_deco = SecurityDecorator(config)


@app.get("/")
@guard_deco.require_ip(whitelist=["192.168.1.0/24", "127.0.0.1/24"])
async def read_root():
    """Root endpoint for health check and welcome message."""
    return {"message": "Hello, World!"}


app.include_router(transaction_router)

# Add global middleware
app.add_middleware(SecurityMiddleware, config=config)

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
