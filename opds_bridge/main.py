from fastapi import FastAPI
from opds_bridge.api.router import router as opds_router
from opds_bridge.api.acquire import router as acquire_router

def create_app() -> FastAPI:
    app = FastAPI(title="Audiobookshelf OPDS Bridge")
    app.include_router(opds_router)
    app.include_router(acquire_router)
    return app

app = create_app()
