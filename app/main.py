from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import authors, withdrawals
from .database import engine, Base

# Create tables if they don't exist (though seed_data.py already does this)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RoyaltyFlow API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(authors.router)
app.include_router(withdrawals.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to RoyaltyFlow API. Access /docs for documentation."}
