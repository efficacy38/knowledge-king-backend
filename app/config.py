from web3 import Web3
from dotenv import load_dotenv
import os
import json
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import SignAndSendRawMiddlewareBuilder
from web3.contract import Contract

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
wb3 = Web3(Web3.HTTPProvider(CELO_RPC_URL))

# Check if the connection is successful - using is_connected() instead of isConnected()
if not wb3.is_connected():
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
gaming_contract: Contract = wb3.eth.contract(
    address=os.getenv('KNOWLEDGE_KING_GAME_CONTRACT_ADDR'),  # Replace with your contract's address
    abi=knowking_abi
)
token_contract: Contract = wb3.eth.contract(
    address=os.getenv('KNOWLEDGE_KING_TOKEN_CONTRACT_ADDR'),  # Replace with your token contract's address
    abi=token_abi )

account_private_key = os.getenv('ACCOUNT_PRIVATE_KEY')
assert account_private_key is not None, "ACCOUNT_PRIVATE_KEY must be set in the environment variables"
assert account_private_key.startswith("0x"), "ACCOUNT_PRIVATE_KEY must start with '0x'"

account: LocalAccount = wb3.eth.account.from_key(account_private_key)
wb3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account), layer=0)

print("current address: ", account.address)
print("current balance: ", wb3.eth.get_balance(account.address))

# debug
gaming_contract.functions.play.transact()
