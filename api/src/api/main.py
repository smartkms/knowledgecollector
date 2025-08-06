import uvicorn
from fastapi import FastAPI
from api.routes import router as subscription_router
from api.auth import setup_auth  # JWT middleware, if needed

app = FastAPI()
setup_auth(app)
app.include_router(
    subscription_router, prefix="/api/subscriptions", tags=["subscriptions"]
)

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000)
