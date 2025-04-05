# Load unified configuration from JSON
CHAIN := $(or $(chain), celo_alfaj) # Default to testnet if no flag is provided
RPC_URL := $(shell cat celo_config.json | jq -r '.networks.$(CHAIN).rpc_url')

# Load private key from environment variable
PRIVATE_KEY := $(shell printenv CELO_PRIVATE_KEY)

deploy:
	cd knowledge-king-contract && forge script script/Knowking.s.sol --rpc-url ${RPC_URL} --private-key ${PRIVATE_KEY} --broadcast

build:
	cd knowledge-king-contract && forge build
