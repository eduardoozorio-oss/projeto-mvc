from app.database import Session
from app.models.usuario import Usuario
from app.auth import hash_senha


USUARIOS = [
    {
        "nome": "Admin",
        "email": "adimin@teste.com",
        "senha": "admin123",
        "role": "admin",
        
    },
]

[
    {
        "nome": "Gabriel",
        "email": "adimingabriel@teste.com",
        "senha": "admin123",
        "role": "admin",
        
    },
]

def criar_usuarios():
    db = Session()
    try:
        for user in USUARIOS:
            existente = db.query(Usuario).filter_by(email=user["email"]).first()
            if existente:
                print(f"Esse e-mail {user["email"]} já está cadastrado no db")
                continue
            else:
                novo_usuario = Usuario(
                    nome=user["nome"],
                    email=user["email"],
                    senha_hash=hash_senha(user["senha"]),
                    role=user["role"]
                )
                db.add(novo_usuario)
                print(f"Usuario cadastrado com sucesso: {user["nome"]}")
        db.commit()

    except Exception as erro:
        db.rollback()
        print("erro")
    finally:
        db.close()

criar_usuarios()