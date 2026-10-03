from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes import router


settings = get_settings()


app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description=(
        "Generate five-panel AI comics using "
        "Gemini and Stable Diffusion."
    ),
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            settings.root_dir / "static"
        )
    ),
    name="static",
)


app.include_router(router)