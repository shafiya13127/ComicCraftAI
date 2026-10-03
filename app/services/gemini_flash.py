import json

from app.config import Settings
from app.schemas import (
    OutlineResponse,
    PromptRequest,
)


def _client(settings: Settings):

    from google import genai

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured"
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_outline(
    request: PromptRequest,
    settings: Settings,
) -> OutlineResponse:

    prompt = f"""
Create exactly 5 connected comic panels.

User story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

- Create exactly five panels.
- Keep the same protagonist throughout.
- Maintain visual continuity.
- Create a clear beginning.
- Develop the story.
- Include a meaningful climax.
- End the story.
- Give each panel a concise title.
- Give each panel a scene description.
- Give each panel an image generation prompt.
- Image prompts must describe visible subjects,
  composition, lighting and environment.
- Do not place written text in generated images.
- Do not include speech bubbles.
- Do not include logos.
- Do not include watermarks.
""".strip()

    from google.genai import types

    client = _client(settings)

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="application/json",
            response_schema=OutlineResponse,
        ),
    )

    raw = response.text or ""

    try:

        data = json.loads(raw)

        return OutlineResponse.model_validate(
            data
        )

    except Exception as exc:

        raise RuntimeError(
            "Gemini returned an invalid outline: "
            f"{exc}"
        ) from exc