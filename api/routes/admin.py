from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.services.mailing import MailingService

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def mailings(request: Request, service: MailingService = Depends()):
    mailings = await service.list()
    return templates.TemplateResponse("admin.html", {"request": request, "mailings": mailings})

