# backend/settings.py
# -------------------
# Centralized settings for the backend.
# Reads environment variables once at startup so the rest of the app
# can stay clean and provider-agnostic.

import os
from dotenv import load_dotenv

# Load variables from a .env file at project root (backend/.env)
load_dotenv()

# Which LLM provider to use: "openai" or "groq"
PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower()

# API keys (supply at least the one you plan to use)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Default models (override in .env if you want different ones)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Allowed frontend origin during local dev (Vite)
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
