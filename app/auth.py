# 1. Hash e verificação de senhas com bcrypt
# 2. Geração de token JWT
# 3. Leitura e validação do token vindo do cookie

from datetime import datetime, timedelta, timezone
from jose import JWSError, jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")


# ERRADO:
# os.getenv retorna STRING
# timedelta(minutes=...) precisa receber INT

# ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


# CERTO:
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

#CryptContext - configura o bcrypt como algoritmo de hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Funções de senha
def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)

#Funções do token - JWT

def criar_token(data: dict):
    payload = data.copy()

    #Define quando o token vai expirar
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})

    #Criar o token jwt
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decodificar_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

#Dependências do FastAPI 

def get_usuario_logado(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    
    try:
        payload = decodificar_token(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Invalido ou expirado"
            )
        return payload
    except JWSError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
def get_usuario_opcional(request: Request):

    try:
        return get_usuario_logado(request)
    except HTTPException:
        return None