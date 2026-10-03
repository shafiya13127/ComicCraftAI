from app.config import Settings
from app.schemas import PromptRequest

from app.services.demo_data import (
    demo_outline,
    demo_story,
)

from app.services.exporters import (
    save_pdf,
)

from app.services.gemini_flash import (
    generate_outline,
)

from app.services.gemini_pro import (
    generate_story,
)

from app.services.image_generator import (
    generate_image,
)

from app.services.layout_builder import (
    build_comic_layout,
)


def generate_comic(
    request: PromptRequest,
    settings: Settings,
) -> tuple[list[dict], str]:

    # --------------------------------
    # STEP 1: Generate outline
    # --------------------------------

    if settings.demo_mode:

        outline = demo_outline(
            request
        )

        story = demo_story(
            request,
            outline,
        )

    else:

        outline = generate_outline(
            request,
            settings,
        )

        # --------------------------------
        # STEP 2: Generate story
        # --------------------------------

        story = generate_story(
            request,
            outline,
            settings,
        )

    # --------------------------------
    # STEP 3: Generate images
    # --------------------------------

    image_paths = []

    for panel in story.panels:

        image_path = generate_image(
            panel.image_prompt,
            settings,
            panel.panel_number,
        )

        image_paths.append(
            image_path
        )

    # --------------------------------
    # STEP 4: Build layout
    # --------------------------------

    layout = build_comic_layout(
        story,
        image_paths,
    )

    # --------------------------------
    # STEP 5: Export PDF
    # --------------------------------

    pdf_path = save_pdf(
        layout,
        settings,
    )

    return layout, pdf_path