import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.db.base_class import Base
from app.db.seed import seed_db
from app.api.v1.router import api_router

# Import models so SQLAlchemy registers them with Base.metadata before creating tables
from app.models.accommodation import Accommodation
from app.models.food_service import FoodService
from app.models.fast_food_spot import FastFoodSpot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing database schema...")
    async with engine.begin() as conn:
        # Create all tables if they do not exist
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Checking database for seed data...")
    async with SessionLocal() as db:
        await seed_db(db)
        
    yield
    
    # Shutdown actions
    logger.info("Shutting down and disposing database connection engine...")
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Standard CORS Middleware setup for integration ease
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}!",
        "docs": "/docs",
        "version": "1.0.0"
    }
