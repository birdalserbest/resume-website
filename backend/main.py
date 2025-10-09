from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow local React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/resume")
def resume():
    # temporary stub; we’ll swap this with your real data later
    return {
        "name": "Your Name",
        "title": "Software Engineer",
        "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
        "projects": [
            {"name": "Project A", "desc": "What it does…", "link": "#"},
            {"name": "Project B", "desc": "What it does…", "link": "#"},
        ],
    }


@app.get("/")
def root():
    return {"message": "Backend is running!"}
