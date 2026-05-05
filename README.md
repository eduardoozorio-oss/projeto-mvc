# instalar o requiremesnts

pip install -r requirements.txt


# Inicializar o alembic

python -m alembic init migrations

# Gerar a migrations
python -m alembic revision --autogenerate -m "Criar tabela usuario"


# Aplicar a migrations
python -m alembic upgrade head