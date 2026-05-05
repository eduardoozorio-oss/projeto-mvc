# 1. Hash e verificação de senhas com bcrypt
#
#

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
import os 

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")


ALGORITHM = os.getenv("ALGORITHM")


ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUT")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha:str):
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)


#Funções do token - JWT
def criar_token(data: dict):
    payload = data.copy()

    #define quando o token expira
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})


    # criar o token jwt
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token 

def decodificar_token(token: str):
    payload = jwt.encode(token, SECRET_KEY, algorithm=[ALGORITHM])
    return payload


