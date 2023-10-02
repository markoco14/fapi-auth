from fastapi import FastAPI
from core.security import JWTAuth
from auth.routes import router as auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from users.routes import router as guest_router, user_router
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings

settings = get_settings()

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)


# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

if settings.ENVIRONMENT == 'prod':
	origins = [
		f"{settings.NEXT_DEMO_URL}",
	]
else :
	origins = [
		"http://localhost",
		"http://localhost:3000",
		"http://127.0.0.1"
		"http://127.0.0.1:3000",
	]

# CORS POLICY

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
	return {"status": "healthy"}       

