from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1 import auth, upload, products, customers, orders
from app.utils.sys import get_db
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Actions on startup
    print("API starting up...")
    
    # Schedule the job to run every minute
    # You might want to adjust the interval based on your needs
    # deposito_service = DepositoService(None) # db will be passed in check_due_depositos
    # scheduler.add_job(deposito_service.check_due_depositos, 'interval', minutes=1, args=[get_db])

    yield
    # Actions on shutdown
    print("API shutting down...")

app = FastAPI(
    title="TEMP DASHBOARD API",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)