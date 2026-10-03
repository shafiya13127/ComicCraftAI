import json

from app.config import Settings

from app.schemas import (
    OutlineResponse,
    PromptRequest,
    StoryResponse,
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


def generate_story(
    request: PromptRequest,
    outline: OutlineResponse,
    settings: Settings,
) -> StoryResponse:

    prompt = f"""
Expand the supplied five-panel outline
into a polished comic script.

Story prompt:
{request.story_prompt}

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Outline JSON:

{outline.model_dump_json(indent=2)}

Requirements:

- Preserve panel order.
- Preserve plot continuity.
- Keep the character consistent.
- Provide a title for every panel.
- Provide a scene description.
- Provide an ambient caption.
- Provide narration.
- Provide dialogue.
- Provide an image prompt.
- Dialogue must be short enough for a comic.
- Make the story engaging.
- Keep the requested tone.
- Image prompts should contain visual information only.
- Do not request written text inside images.
""".strip()

    from google.genai import types

    client = _client(settings)

    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
            response_schema=StoryResponse,
        ),
    )

    raw = response.text or ""

    try:

        data = json.loads(raw)

        return StoryResponse.model_validate(
            data
        )

    except Exception as exc:

        raise RuntimeError(
            "Gemini returned an invalid story: "
            f"{exc}"
        ) from exc