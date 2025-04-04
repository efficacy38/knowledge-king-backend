from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration settings for the application
QUESTIONS_FILE_PATH = os.getenv("QUESTIONS_FILE_PATH", "questions.json")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quizzes.db")

# Connect to the Ethereum node (replace with your provider URL)
provider_url = os.getenv("PROVIDER_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")
web3 = Web3(Web3.HTTPProvider(provider_url))

# Check if the connection is successful
if not web3.isConnected():
    print("Failed to connect to the Ethereum network")
    exit()

# Replace with your contract's address and ABI
contract_address = os.getenv("CONTRACT_ADDRESS", "0xYourContractAddress")
contract_abi = [
    # Add your contract's ABI here
]

# Create a contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
