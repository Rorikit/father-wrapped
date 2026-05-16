import json
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from app.main import app


ROOT_DIR = Path(__file__).resolve().parents[1]


def test_home_page_renders_wrapped_story():
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "Папа Wrapped" in response.text
    assert "/static/css/styles.css" in response.text
    assert "/static/js/app.js" in response.text


def test_static_assets_are_served():
    client = TestClient(app)

    css_response = client.get("/static/css/styles.css")
    js_response = client.get("/static/js/app.js")
    image_response = client.get("/static/media/photos/demo-memory.svg")

    assert css_response.status_code == 200
    assert ".story-shell" in css_response.text
    assert js_response.status_code == 200
    assert "progressBar" in js_response.text
    assert image_response.status_code == 200
    assert "image/svg+xml" in image_response.headers["content-type"]


def test_missing_page_uses_custom_404_template():
    response = TestClient(app).get("/missing-page")

    assert response.status_code == 404
    assert "Страница не найдена" in response.text
    assert "Вернуться к началу" in response.text


def test_memories_json_has_required_sections_and_existing_demo_images():
    data = json.loads((ROOT_DIR / "app" / "data" / "memories.json").read_text(encoding="utf-8"))

    for key in [
        "meta",
        "hero",
        "stats",
        "top_moments",
        "eras",
        "favorites",
        "quotes",
        "gallery",
        "messages",
        "final",
    ]:
        assert key in data

    image_paths = [data["hero"]["portrait"]]
    image_paths.extend(moment["photo"] for moment in data["top_moments"])
    image_paths.extend(era["cover"] for era in data["eras"])
    image_paths.extend(item["photo"] for item in data["gallery"])

    for url_path in image_paths:
        assert url_path.startswith("/static/")
        local_path = ROOT_DIR / "app" / "static" / url_path.removeprefix("/static/")
        assert local_path.exists()


def test_render_start_command_uses_port_environment_variable():
    config = yaml.safe_load((ROOT_DIR / "render.yaml").read_text(encoding="utf-8"))
    service = config["services"][0]

    assert service["type"] == "web"
    assert service["env"] == "python"
    assert service["buildCommand"] == "pip install -r requirements.txt"
    assert service["startCommand"] == "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
