SET UP

```
git clone
pip install -r requirements.txt
alembic revision --autogenerate -m "Create users table"
alembic upgrade head
SECRET_KEY = openssl rand -hex 32
uvicorn main:app --reload
```
