import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.log_settings import initialize_logging
from src.config.server_settings import get_uvicorn_config

# Initialize logging configuration
initialize_logging()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


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
