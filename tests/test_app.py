import os

# Force demo mode for tests.
os.environ["DEMO_MODE"] = "true"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_homepage():

    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ok"


def test_json_generation_demo():

    payload = {
        "story_prompt": (
            "A brave fox explores "
            "an enchanted forest."
        ),
        "character_name": "Milo",
        "setting": "forest",
        "tone": "funny",
        "art_style": "comic book",
    }

    response = client.post(
        "/generate-comic/json",
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True

    assert len(
        body["layout"]
    ) == 5

    assert body[
        "pdf_path"
    ].endswith(".pdf")