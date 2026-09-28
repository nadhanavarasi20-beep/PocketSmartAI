# PocketSmart AI — Your Smart Budget & Recommendation Assistant

A GenAI-powered budgeting assistant built with **FastAPI** + **Gemini 1.5 Flash Pro** that generates
personalized, budget-aware recommendations across three domains:

- **Home Interior Planner** — furniture, lighting, decor (IKEA, Amazon)
- **Party Budget Planner** — catering, venue, decoration, entertainment (Swiggy, Zomato, OYO, Amazon)
- **Jewelry Budget Planner** — jewelry matched to occasion & outfit color, with optional image upload
  (Amazon, Flipkart)

It includes user registration/login (JWT + hashed passwords), a dashboard, recommendation history,
and a JSON-file "database" so it runs immediately with zero external DB setup.

If the Gemini API is unreachable or no key is configured, every planner automatically falls back to a
locally computed estimate, so the app never breaks mid-demo.

---

## 1. Project structure

```
pocketsmart-ai/
├── main.py                  # FastAPI app entry point (routes, CORS, startup)
├── requirements.txt
├── .env.example              # copy to .env and fill in your keys
├── app/
│   ├── auth.py               # password hashing, JWT issue/verify, current-user dependency
│   ├── database.py           # lightweight JSON-file user & history store
│   ├── gemini_utils.py       # prompt building, Gemini calls, JSON parsing, fallback logic
│   ├── models.py             # Pydantic request/response schemas
│   └── routes/
│       ├── auth_routes.py    # /register /login /logout /token /session-info /session-data
│       └── planner_routes.py # /dashboard /planner/* /generate-* /history
├── templates/                # Jinja2 HTML templates
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── uploads/               # uploaded outfit photos are saved here
└── data/                      # users.json / history.json created automatically at runtime
```

## 2. Setup

**Requirements:** Python 3.10+

```bash
# 1. Open this folder in VS Code, then in a terminal:
cd pocketsmart-ai

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env       # Windows
cp .env.example .env         # macOS / Linux
```

Open `.env` and set:

```
GEMINI_API_KEY=your_real_key_from_https://aistudio.google.com/app/apikey
SECRET_KEY=any_long_random_string
```

> The app runs fine **without** a real Gemini key — it will just serve fallback recommendations and
> print a warning on startup. Add a key for live, personalized AI output.

## 3. Run

```bash
uvicorn main:app --reload
```

or

```bash
python main.py
```

Then open **http://127.0.0.1:8000** in your browser.

## 4. Using the app

1. Go to `/register` and create an account, then `/login`.
2. From `/dashboard`, open any of the three planners.
3. Fill in the budget form and submit — you'll see AI-generated, itemized recommendations with
   per-item budgets, suggested platforms, and tips.
4. Visit `/history` to review everything you've generated.

### API-only usage

The app also exposes a standard OAuth2 password-flow token endpoint for programmatic/API access:

```bash
curl -X POST http://127.0.0.1:8000/token \
  -d "username=yourname&password=yourpassword"
```

Use the returned `access_token` as a `Authorization: Bearer <token>` header on `/session-info`,
`/session-data`, or any `/generate-*` endpoint.

Interactive API docs are available at **http://127.0.0.1:8000/docs**.

## 5. Notes for the writeup / viva

- **Gemini AI Layer:** all prompt construction and response parsing lives in `app/gemini_utils.py`
  (`get_home_recommendations`, `get_party_recommendations`, `get_jewelry_recommendations`). Gemini is
  asked to return strict JSON, which is parsed defensively (`_extract_json`) and falls back to a
  deterministic local estimate if parsing or the API call fails.
- **Auth:** `app/auth.py` issues JWTs (`python-jose`) and stores bcrypt-hashed passwords
  (`passlib`). Tokens are read from either an httponly cookie (browser UI) or an `Authorization`
  header (API clients).
- **Storage:** `app/database.py` is a minimal JSON-file store, intentionally swappable for a real
  database later without changing any route code.
- **Multimodal input:** the Jewelry Planner accepts an optional outfit image (`UploadFile`), saves it
  under `static/uploads/`, and passes the raw bytes to Gemini as a `PIL.Image` alongside the text
  prompt for color-aware suggestions.
