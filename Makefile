# Load unified configuration from JSON
CONFIG := $(shell cat celo_config.json)
CHAIN := $(or $(chain), celo_alfaj) # Default to testnet if no flag is provided
RPC_URL := $(shell echo $(CONFIG) | jq -r '.rpc_urls."$(CHAIN)"')

# Load private key from environment variable
PRIVATE_KEY := $(shell printenv CELO_PRIVATE_KEY)

deploy:
	forge script script/Knowking.s.sol:KnowkingScript --rpc-url ${RPC_URL} --private-key ${PRIVATE_KEY} --broadcast

build:
	cd knowledge-king-contract && forge build
