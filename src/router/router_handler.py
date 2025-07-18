from src.router.debug_router import router as debug_router
from src.router.debug_view import router as debug_view_router


def register_debug_routers(app):
    app.include_router(debug_router)
    app.include_router(debug_view_router)
