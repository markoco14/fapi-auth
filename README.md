SET UP

# Directory
git clone https://github.com/markoco14/fast-auth-api.git your-directory-name
cd your-directory-name
python -m venv venv (or python3 -m)
source venv/bin/activate
pip install -r requirements.txt


# Database
mysql -u your-user-name -p your-password
create database your-database-name
exit

# .env
fill in your db credentials
generate jwt secret in terminal with openssl rand -hex 32
choose your production url (can do it later when ready to deploy)

# Migrations
change __tablename__ in UserModel as desired ie; "app_users, users, test_users"
add fields as needed "is_admin, membership"
alembic revision --autogenerate -m "Create users table"
alembic upgrade head
uvicorn main:app --reload

