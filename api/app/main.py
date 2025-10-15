from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, screener, ticker, weekly, search

app = FastAPI(title="Tintel API")

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Routers ===
app.include_router(health.router)
app.include_router(screener.router)
app.include_router(ticker.router)
app.include_router(weekly.router)
app.include_router(search.router)


@app.get("/")
def root():
    return {"message": "Tintel backend running"}
