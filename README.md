SET UP

```
git clone
pip install -r requirements.txt
alembic revision --autogenerate -m "Create users table"
alembic upgrade head
JWT_SECRET = openssl rand -hex 32
uvicorn main:app --reload
```
