"""
PocketSmart AI - FastAPI entry point.

Run with:
    uvicorn main:app --reload

Or simply:
    python main.py
"""
import os

from dotenv import load_dotenv

load_dotenv()  # must happen before app.gemini_utils reads GEMINI_API_KEY

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.auth import get_current_user_optional
from app.routes import auth_routes, planner_routes

app = FastAPI(
    title="PocketSmart AI",
    description="Your Smart Budget & Recommendation Assistant",
    version="1.0.0",
)

# --------------------------------------------------------------- CORS -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------- static & views ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ------------------------------------------------------------- routers ----
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(planner_routes.router, tags=["planners"])


# ---------------------------------------------------------- public pages --
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = await get_current_user_optional(request)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.get("/testimonials", response_class=HTMLResponse)
async def testimonials(request: Request):
    user = await get_current_user_optional(request)
    return templates.TemplateResponse("testimonials.html", {"request": request, "user": user})


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "PocketSmart AI"}


# ---------------------------------------------------------------- events --
@app.on_event("startup")
async def on_startup():
    from app import gemini_utils
    if gemini_utils._model is None:
        print(
            "\n[PocketSmart AI] WARNING: GEMINI_API_KEY is not set (or is a placeholder).\n"
            "The app will still run using local fallback recommendations.\n"
            "Add your key to a .env file (see .env.example) for live Gemini output.\n"
        )
    else:
        print(f"[PocketSmart AI] Gemini model '{gemini_utils.GEMINI_MODEL_NAME}' ready.")
    print("[PocketSmart AI] Startup complete. Visit http://127.0.0.1:8000")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
