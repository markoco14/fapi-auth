SET UP

```
git clone
pip install -r requirements.txt
alembic revision --autogenerate -m "Create users table"
alembic upgrade head
uvicorn main:app --reload
```
