"""Application entrypoint for the Personal Transport API FastAPI backend."""
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from a .env file if present.
load_dotenv()

app = FastAPI(title="Personal Transport API")


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Simple health check endpoint used by monitoring and smoke tests."""
    return {"status": "ok"}
