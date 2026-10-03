from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    FileResponse,
    HTMLResponse,
)

from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.schemas import PromptRequest

from app.services.comic_service import generate_comic
from app.services.image_generator import generate_image


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(
        settings.root_dir / "templates"
    )
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "demo_mode": settings.demo_mode
        },
    )


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):

    try:

        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        layout, pdf_path = generate_comic(
            data,
            settings,
        )

        pdf_url = (
            "/static/exports/"
            + Path(pdf_path).name
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_url": pdf_url,
                "demo_mode": settings.demo_mode,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "error": str(exc)
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_comic_json(
    payload: PromptRequest,
):

    try:

        layout, pdf_path = generate_comic(
            payload,
            settings,
        )

        return {
            "success": True,
            "layout": layout,
            "pdf_path": (
                "/static/exports/"
                + Path(pdf_path).name
            ),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={},
    )


@router.get("/test-image")
async def test_image(
    prompt: str = (
        "a brave fox in an enchanted "
        "forest, comic book art"
    ),
):

    try:

        path = generate_image(
            prompt,
            settings,
            panel_number=0,
        )

        return {
            "success": True,
            "image_url": (
                "/static/"
                + path.removeprefix("static/")
            ),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get("/health")
async def health():

    return {
        "status": "ok",
        "demo_mode": settings.demo_mode,
    }


@router.get("/download/{filename}")
async def download(
    filename: str,
):

    safe_name = Path(filename).name

    path = (
        settings.root_dir
        / settings.export_dir
        / safe_name
    )

    if not path.exists():

        raise HTTPException(
            status_code=404,
            detail="PDF not found",
        )

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=safe_name,
    )