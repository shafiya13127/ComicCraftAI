import hashlib
import re

from pathlib import Path
from threading import Lock

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

from app.config import Settings


_PIPELINE = None
_PIPELINE_LOCK = Lock()


def _safe_name(prompt: str) -> str:

    digest = hashlib.sha256(
        prompt.encode("utf-8")
    ).hexdigest()[:12]

    slug = re.sub(
        r"[^a-zA-Z0-9]+",
        "-",
        prompt.lower(),
    ).strip("-")[:50]

    if not slug:
        slug = "panel"

    return (
        f"{slug}-{digest}.png"
    )


def _demo_image(
    prompt: str,
    output: Path,
    width: int,
    height: int,
) -> str:

    image = Image.new(
        "RGB",
        (width, height),
        "#f4efe3",
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (
            18,
            18,
            width - 18,
            height - 18,
        ),
        outline="#1f2937",
        width=5,
    )

    draw.ellipse(
        (
            width * 0.35,
            height * 0.25,
            width * 0.65,
            height * 0.55,
        ),
        fill="#f59e0b",
        outline="#111827",
        width=4,
    )

    draw.rectangle(
        (
            width * 0.3,
            height * 0.55,
            width * 0.7,
            height * 0.75,
        ),
        fill="#60a5fa",
        outline="#111827",
        width=4,
    )

    font = ImageFont.load_default()

    text = (
        "DEMO IMAGE\n"
        + prompt[:90]
    )

    draw.multiline_text(
        (30, height - 105),
        text,
        fill="#111827",
        font=font,
        spacing=5,
    )

    image.save(
        output,
        format="PNG",
    )

    return output.as_posix()


def _relative_panel_path(
    settings: Settings,
    output: Path,
) -> str:

    return (
        Path(settings.panel_dir)
        / output.name
    ).as_posix()


def _load_pipeline(
    settings: Settings,
):

    global _PIPELINE

    if _PIPELINE is not None:
        return _PIPELINE

    with _PIPELINE_LOCK:

        if _PIPELINE is not None:
            return _PIPELINE

        import torch

        from diffusers import (
            StableDiffusionPipeline,
        )

        if torch.cuda.is_available():

            dtype = torch.float16

        else:

            dtype = torch.float32

        kwargs = {
            "torch_dtype": dtype,
            "use_safetensors": True,
        }

        if settings.hf_token:

            kwargs["token"] = (
                settings.hf_token
            )

        _PIPELINE = (
            StableDiffusionPipeline
            .from_pretrained(
                settings.diffusion_model_id,
                **kwargs,
            )
        )

        if torch.cuda.is_available():

            device = "cuda"

        elif torch.backends.mps.is_available():

            device = "mps"

        else:

            device = "cpu"

        _PIPELINE = _PIPELINE.to(
            device
        )

        return _PIPELINE


def generate_image(
    prompt: str,
    settings: Settings,
    panel_number: int = 1,
) -> str:

    settings.ensure_directories()

    filename = _safe_name(
        f"{panel_number}-{prompt}"
    )

    output = (
        settings.root_dir
        / settings.panel_dir
        / filename
    )

    # Demo mode
    if settings.demo_mode:

        _demo_image(
            prompt,
            output,
            settings.image_width,
            settings.image_height,
        )

        return _relative_panel_path(
            settings,
            output,
        )

    # Real image generation
    if (
        settings.image_provider.lower()
        != "diffusers"
    ):

        raise RuntimeError(
            "Only IMAGE_PROVIDER=diffusers "
            "is implemented."
        )

    pipe = _load_pipeline(
        settings
    )

    result = pipe(
        prompt=prompt,
        width=settings.image_width,
        height=settings.image_height,
        num_inference_steps=settings.image_steps,
        guidance_scale=settings.image_guidance,
    )

    image = result.images[0]

    image.save(
        output,
        format="PNG",
    )

    return _relative_panel_path(
        settings,
        output,
    )