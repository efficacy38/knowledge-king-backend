from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from web3 import Web3

from app.database import engine, Base, get_db
from app.routes.quiz import router as quiz_router
from app.models.quiz import Quiz
from app.config import web3, contract

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

# Define the event to monitor (replace 'YourEventName' with the actual event name)
event_filter = contract.events.YourEventName.createFilter(fromBlock='latest')

print("Listening for events...")

# Monitor the event
while True:
    for event in event_filter.get_new_entries():
        print("Event log:", event)