from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from contextlib import asynccontextmanager

#from .models import ()

from .research_service import ResearchService

load_dotenv()

# Global variable for the research service
research_service: ResearchService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global research_service
    try:
        research_service = ResearchService()
        await research_service.initialize()
    except Exception as e:
        print("Error initializing ResearchService:", e)
        raise

    yield

    if research_service:
        await research_service.shutdown()


app = FastAPI(
    title="Multi-Agent Research Assistant API",
    description="Ultra-fast AI-powered research assistant using Cerebras, Exa, and LlamaIndex",
    version="1.0.0",
    lifespan=lifespan
)
