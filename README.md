# Instalar o requirements.txt

pip install -r requirements.txt

#Inicializar o alembic
python -m alembic init migrations

# Gerar a migration
python -m alembic revision --autogenerate -m "Criar tabela usuario"

# Aplicar a migration
python -m alembic upgrade head

#Rodar o código
python -m uvicorn app.main:app --reload