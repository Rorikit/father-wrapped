import json
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "memories.json"

app = FastAPI(title="Papa Wrapped")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@lru_cache
def load_memories() -> dict:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "wrapped": load_memories(),
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return templates.TemplateResponse(
            request,
            "error.html",
            {
                "status_code": 404,
                "title": "Страница не найдена",
                "message": "Похоже, эта часть истории ещё не записана.",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exc.status_code,
            "title": "Что-то пошло не так",
            "message": "Попробуйте обновить страницу или вернуться к началу истории.",
        },
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": 500,
            "title": "История на секунду задумалась",
            "message": "Обновите страницу, и альбом продолжит работать.",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
