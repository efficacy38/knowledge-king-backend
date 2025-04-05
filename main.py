from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from web3 import Web3

from app.database import engine, Base, get_db
from app.routes.quiz import router as quiz_router
from app.models.quiz import Quiz
from app.config import web3, gaming_contract, token_contract

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

# Define the event to monitor - fixed by adding from_block parameter
# event_filter = gaming_contract.events.startGame.create_filter
# print(type(gaming_contract.events.startGame.create_filter))
event_filter = gaming_contract.events.startGame.create_filter(from_block='latest')
print("Listening for events...")

# print all startGame events from the last 10 blocks
def print_events():
    while True:
        for event in event_filter.get_new_entries():
            print(f"New event: {event}")
        time.sleep(2)  # Adjust the sleep time as needed