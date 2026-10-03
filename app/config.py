from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Gemini
    gemini_api_key: str | None = None
    gemini_outline_model: str = "gemini-3.8-flash"
    gemini_story_model: str = "gemini-2.5-pro"

    # Image generation
    image_provider: str = "diffusers"
    hf_token: str | None = None
    diffusion_model_id: str = (
        "stable-diffusion-v1-5/stable-diffusion-v1-5"
    )

    image_width: int = 512
    image_height: int = 512
    image_steps: int = 20
    image_guidance: float = 7.5

    # Demo mode
    demo_mode: bool = False

    # Application
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    max_panels: int = 5

    # Storage
    panel_dir: str = "static/panels"
    export_dir: str = "static/exports"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def root_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    def ensure_directories(self) -> None:
        panel_path = self.root_dir / self.panel_dir
        export_path = self.root_dir / self.export_dir

        panel_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        export_path.mkdir(
            parents=True,
            exist_ok=True,
        )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings