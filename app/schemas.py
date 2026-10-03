from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    story_prompt: str = Field(
        min_length=5,
        max_length=2000,
    )

    character_name: str = Field(
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        min_length=1,
        max_length=120,
    )

    tone: str = Field(
        min_length=1,
        max_length=80,
    )

    art_style: str = Field(
        min_length=1,
        max_length=80,
    )

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style",
    )
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "This field cannot be empty"
            )

        return value


class PanelOutline(BaseModel):
    panel_number: int = Field(
        ge=1,
        le=10,
    )

    title: str = Field(
        min_length=1,
        max_length=120,
    )

    scene_description: str = Field(
        min_length=1,
        max_length=1000,
    )

    image_prompt: str = Field(
        min_length=1,
        max_length=1500,
    )


class OutlineResponse(BaseModel):
    panels: list[PanelOutline] = Field(
        min_length=5,
        max_length=5,
    )


class PanelStory(BaseModel):
    panel_number: int = Field(
        ge=1,
        le=10,
    )

    title: str = Field(
        min_length=1,
        max_length=120,
    )

    scene_description: str = Field(
        min_length=1,
        max_length=1200,
    )

    caption: str = Field(
        default="",
        max_length=500,
    )

    narration: str = Field(
        default="",
        max_length=1500,
    )

    dialogue: str = Field(
        default="",
        max_length=1500,
    )

    image_prompt: str = Field(
        min_length=1,
        max_length=1800,
    )


class StoryResponse(BaseModel):
    panels: list[PanelStory] = Field(
        min_length=5,
        max_length=5,
    )


class ComicRequest(PromptRequest):
    pass