"""
Page routes for the AI chat application
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Home page with AI chat interface"""
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "AI Chat - FastOpp"
    })


@router.get("/conversation-browser", response_class=HTMLResponse)
async def conversation_browser(request: Request):
    """Conversation browser page with folder management"""
    return templates.TemplateResponse("conversation_browser.html", {
        "request": request,
        "title": "Conversation Browser - FastOpp"
    })