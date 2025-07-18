import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from router.digipos import router as digipos_router
from src.config.log_settings import initialize_logging
from src.config.server_settings import get_uvicorn_config

# Initialize logging configuration
initialize_logging()
app = FastAPI()


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors and return a custom plain text response.

    Parameters
    ----------
    request : Request
        The incoming HTTP request.
    exc : RequestValidationError
        The validation error exception.

    Returns:
    -------
    PlainTextResponse
        A response with status code 422 and a message indicating missing fields.
    """
    missing_fields = [err["loc"][-1] for err in exc.errors()]
    message = f"{', '.join(missing_fields)} wajib diisi"
    return PlainTextResponse(
        content=f"status=91&message={message}",
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the Digipos router
app.include_router(digipos_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/")
async def read_root():
    """Root endpoint for health check and welcome message."""
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    config = get_uvicorn_config()
    uvicorn.run(
        app="src.main:app",
        host=str(config["host"]),
        port=int(config["port"]),
        reload=bool(config["reload"]),
    )
