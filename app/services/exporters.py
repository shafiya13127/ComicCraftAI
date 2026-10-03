from datetime import datetime
from pathlib import Path
import os

from fpdf import FPDF

from app.config import Settings


def _find_font() -> str | None:

    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]

    for path in candidates:

        if os.path.exists(path):
            return path

    return None


def save_pdf(
    layout: list[dict],
    settings: Settings,
) -> str:

    settings.ensure_directories()

    filename = (
        "comiccraft-"
        + datetime.now().strftime(
            "%Y%m%d-%H%M%S-%f"
        )
        + ".pdf"
    )

    output = (
        settings.root_dir
        / settings.export_dir
        / filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    font = _find_font()

    if font:

        pdf.add_font(
            "DejaVu",
            "",
            font,
        )

        pdf.add_font(
            "DejaVu",
            "B",
            font,
        )

        family = "DejaVu"

    else:

        family = "Helvetica"

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            family,
            "B",
            18,
        )

        pdf.multi_cell(
            0,
            10,
            (
                f"Panel "
                f"{panel['panel_number']}: "
                f"{panel['title']}"
            ),
        )

        pdf.ln(3)

        image_path = (
            settings.root_dir
            / panel["image_path"]
        )

        if image_path.exists():

            max_width = 175

            x = (
                210 - max_width
            ) / 2

            pdf.image(
                str(image_path),
                x=x,
                w=max_width,
            )

            pdf.ln(5)

        pdf.set_font(
            family,
            "",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            panel["scene_description"],
        )

        if panel["caption"]:

            pdf.ln(2)

            pdf.set_font(
                family,
                "B",
                11,
            )

            pdf.multi_cell(
                0,
                7,
                "Caption: "
                + panel["caption"],
            )

        if panel["narration"]:

            pdf.ln(2)

            pdf.set_font(
                family,
                "",
                11,
            )

            pdf.multi_cell(
                0,
                7,
                "Narration: "
                + panel["narration"],
            )

        if panel["dialogue"]:

            pdf.ln(2)

            pdf.set_font(
                family,
                "B",
                11,
            )

            pdf.multi_cell(
                0,
                7,
                "Dialogue: "
                + panel["dialogue"],
            )

    pdf.output(
        str(output)
    )

    return output.as_posix()