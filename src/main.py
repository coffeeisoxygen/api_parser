import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from guard import SecurityDecorator, SecurityMiddleware

from src.config.log_settings import initialize_logging
from src.config.security_settings import SecurityConfig
from src.config.server_settings import get_uvicorn_config
from src.exceptions.oto_exceptions import OtoExceptionError
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


@app.exception_handler(OtoExceptionError)
async def oto_exception_handler(request: Request, exc: OtoExceptionError):
    return exc.render()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Ambil error message dari exc.errors()
    messages = []
    for err in exc.errors():
        loc = ".".join(str(loc_part) for loc_part in err["loc"])
        msg = err["msg"]
        messages.append(f"{loc}: {msg}")
    # Gabungkan pesan error
    message = "; ".join(messages)
    # Format plain text OtomaX
    return PlainTextResponse(content=f"status=422&message={message}", status_code=422)


# NOTE : aktifin mereka kalau nanti udah punya FE
# @app.exception_handler(AppExceptionError)
# async def app_exception_handler_fastapi(request: Request, exc: AppExceptionError):
#     return app_exception_handler(exc)

# @app.exception_handler(ItemNotFoundError)
# async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
#     return app_exception_handler(exc)
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
