from fastapi import FastAPI
from core.security import JWTAuth
from auth.routes import router as auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from users.routes import router as guest_router, user_router
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)


# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


# CORS POLICY
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1"
    "http://127.0.0.1:3000",
]

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

