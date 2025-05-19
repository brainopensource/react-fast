import asyncio
from fastapi import FastAPI

from app.infrastructure.di.container import DIContainer
from app.presentation.api.api_setup import setup_api


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Hexagonal FastAPI App")
    
    # Create the DI container
    container = DIContainer()
    
    # Setup API routes
    setup_api(app, container)
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
