from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Claim Processing Pipeline")

app.include_router(router)