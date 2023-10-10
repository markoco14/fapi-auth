from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.routes import router as auth_router
from core.config import get_settings
from users.routes import router as guest_router, user_router

settings = get_settings()

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)



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
