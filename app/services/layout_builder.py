from typing import Any


def build_comic_layout(
    story: dict[str, Any],
    image_paths: list[str],
) -> list[dict[str, Any]]:
    """
    Combine the generated story panels with their generated image paths
    to create the final comic layout.
    """

    panels = story.get("panels", [])
    layout = []

    for index, panel in enumerate(panels):
        image_path = image_paths[index] if index < len(image_paths) else ""

        layout.append(
            {
                "panel_number": panel.get("panel_number", index + 1),
                "title": panel.get("title", f"Panel {index + 1}"),
                "image_path": image_path,
                "scene_description": panel.get(
                    "scene_description", ""
                ),
                "caption": panel.get("caption", ""),
                "narration": panel.get("narration", ""),
                "dialogue": panel.get("dialogue", ""),
                "image_prompt": panel.get("image_prompt", ""),
            }
        )

    return layout