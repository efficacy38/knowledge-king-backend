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

# Check if the connection is successful - using is_connected() instead of isConnected()
if not web3.is_connected():
    print("Failed to connect to the Celo network")
    exit()

# Load the ABI for Knowking.sol
try:
    with open("./Knowking.sol/KnowledgeKingGame.json", "r") as f:
        knowking_abi = json.load(f)["abi"]
except FileNotFoundError:
    print("KnowledgeKingGame.json not found at expected location")
    knowking_abi = []

# Load the ABI for Token.sol
try:
    with open("./Token.sol/KnowledgeKingToken.json", "r") as f:
        token_abi = json.load(f)["abi"]
except FileNotFoundError:
    print("KnowledgeKingToken.json not found at expected location")
    token_abi = []

# Replace with your contract's address (must be a valid address, not just a placeholder)

# Replace with your contract's address (must be a valid address, not just a placeholder)
gaming_contract = web3.eth.contract(
    address=os.getenv('KNOWLEDGE_KING_GAME_CONTRACT_ADDR'),  # Replace with your contract's address
    abi=knowking_abi
)
token_contract = web3.eth.contract(
    address=os.getenv('KNOWLEDGE_KING_TOKEN_CONTRACT_ADDR'),  # Replace with your token contract's address
    abi=token_abi )
