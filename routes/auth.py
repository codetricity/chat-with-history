"""
Authentication routes for the AI chat application
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login",
        "current_page": "login"
    })


@router.post("/login")
async def login_form(request: Request):
    """Handle login form submission"""
    # Simple redirect for now - can be expanded later
    return RedirectResponse(url="/", status_code=302)