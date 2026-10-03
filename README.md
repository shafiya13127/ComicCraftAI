# ComicCraft - AI Comic Story Creator

ComicCraft is an AI-powered web application that converts a
user's story idea into a five-panel comic.

The application uses:

- FastAPI
- Jinja2
- Gemini
- Stable Diffusion
- Hugging Face Diffusers
- Pillow
- FPDF2

---

# Features

- Story prompt input
- Character name
- Setting selection
- Story tone
- Art style
- Five-panel story generation
- AI narration
- AI dialogue
- AI image prompts
- Stable Diffusion illustrations
- Comic preview
- PDF export
- REST API
- Swagger API documentation
- Demo mode
- Automated tests

---

# Project Structure

```text
ComicCraft/
│
├── app/
│   ├── config.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   │
│   └── services/
│       ├── comic_service.py
│       ├── demo_data.py
│       ├── exporters.py
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       └── layout_builder.py
│
├── templates/
├── static/
├── tests/
├── .env.example
├── requirements.txt
├── run.py
└── README.md