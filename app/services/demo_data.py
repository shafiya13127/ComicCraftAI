from app.schemas import (
    OutlineResponse,
    PanelOutline,
    PanelStory,
    PromptRequest,
    StoryResponse,
)


def demo_outline(
    request: PromptRequest,
) -> OutlineResponse:

    names = [
        "The Call",
        "Into the Wild",
        "The Test",
        "The Turning Point",
        "Home Again",
    ]

    scenes = [
        (
            f"{request.character_name} discovers "
            f"a mysterious clue in {request.setting}."
        ),
        (
            f"{request.character_name} follows "
            f"the clue deeper into {request.setting}."
        ),
        (
            f"A surprising obstacle challenges "
            f"{request.character_name}'s courage."
        ),
        (
            f"{request.character_name} finds a clever "
            f"way through the obstacle."
        ),
        (
            f"{request.character_name} returns with "
            f"a new understanding of the adventure."
        ),
    ]

    panels = []

    for index in range(5):

        panels.append(
            PanelOutline(
                panel_number=index + 1,
                title=names[index],
                scene_description=scenes[index],
                image_prompt=(
                    f"{request.art_style} comic panel, "
                    f"{scenes[index]}, "
                    "cinematic composition, "
                    "expressive character, "
                    "detailed environment, "
                    "no text"
                ),
            )
        )

    return OutlineResponse(
        panels=panels
    )


def demo_story(
    request: PromptRequest,
    outline: OutlineResponse,
) -> StoryResponse:

    panels = []

    for panel in outline.panels:

        panels.append(
            PanelStory(
                panel_number=panel.panel_number,
                title=panel.title,
                scene_description=(
                    panel.scene_description
                ),
                caption=(
                    f"A {request.tone} moment "
                    f"in {request.setting}."
                ),
                narration=(
                    f"{request.character_name} "
                    "takes the next step, guided "
                    "by the mystery introduced "
                    "in the story."
                ),
                dialogue=(
                    f'{request.character_name}: '
                    '"I can do this."'
                ),
                image_prompt=panel.image_prompt,
            )
        )

    return StoryResponse(
        panels=panels
    )