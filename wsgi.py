import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"

for site_packages in [
    *VENV_DIR.glob("lib/python*/site-packages"),
    VENV_DIR / "Lib" / "site-packages",
]:
    if site_packages.exists():
        sys.path.insert(0, str(site_packages))

sys.path.insert(0, str(PROJECT_DIR))

from a2wsgi import ASGIMiddleware

from app.main import app


# SpaceWeb shared hosting runs Python apps through Apache mod_wsgi.
# FastAPI is ASGI, so this adapter exposes it as a WSGI callable.
application = ASGIMiddleware(app)
