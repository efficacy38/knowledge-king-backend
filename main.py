from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes.quiz import router as quiz_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Knowledge King API",
    description="API for quiz questions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quiz_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Knowledge King API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)