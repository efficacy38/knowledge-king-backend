from web3 import Web3
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Load unified configuration from JSON file
with open("celo_config.json", "r") as f:
    config = json.load(f)

DATABASE_URL = config.get("database_url", "sqlite:///./quizzes.db")
QUESTIONS_FILE_PATH = config.get("questions_file_path", "questions.json")

# Select network configuration
network_key = os.getenv("CELO_NETWORK", "celo_alfaj")
network_config = config["networks"].get(network_key, {})
CELO_RPC_URL = network_config.get("rpc_url", "")

if not CELO_RPC_URL:
    print(f"Invalid configuration for network: {network_key}")
    exit()

# Update Web3 provider to use the selected RPC URL
web3 = Web3(Web3.HTTPProvider(CELO_RPC_URL))

# Check if the connection is successful
if not web3.isConnected():
    print("Failed to connect to the Celo network")
    exit()

# Replace with your contract's address and ABI
contract_address = os.getenv("CONTRACT_ADDRESS", "0xYourContractAddress")
contract_abi = [
    # Add your contract's ABI here
]

# Create a contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
