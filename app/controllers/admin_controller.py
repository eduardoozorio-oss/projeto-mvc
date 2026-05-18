from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario

from app.auth import get_admin, hash_senha

#APIROUTER agrupa as rotas desse arquivo com o prefixo /auth
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

#configura para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")

#Listar todos os usuarios
@router.get("/")
def listar_usuarios(
    request: Request,
    db: Session = Depends(get_db),
    admin = Depends(get_admin),


):
    
    #Pegar todos os usuarios do banco de dados
    usuarios = db.query(Usuario).order_by(Usuario.id).all()
    
    return templates.TemplateResponse(
        request,
        "usuarios/index.html",
        {
            "request": request,
            "admin": admin,
            "usuarios": usuarios
        }
)