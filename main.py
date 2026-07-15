from fastapi import FastAPI

from app.core.config import get_settings
from app.routes.grammar import router as grammar_router
from app.routes.health import router as health_router

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", description="Explainable German grammar feedback API")
app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(grammar_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Visit /docs for interactive API documentation."}
