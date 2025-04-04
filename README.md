# knoledge-king-backend

## How to Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd knoledge-king-backend
   ```

2. **Install Dependencies**
   - Use `uv` as the virtual environment provider:
     ```bash
     uv install
     ```
   - For Solidity contracts:
     ```bash
     cd knowledge-king-contract
     forge install
     ```

3. **Set Environment Variables**
   Create a `.env` file from `.env.sample` in the root directory and add the following:
   ```env
   CELO_PRIVATE_KEY=<your-private-key>
   ```

4. **Configure Deployment**
   Update `celo_config.json` with the appropriate RPC URLs for testnet and mainnet(if you needed, Optional):
   ```json
   {
       "rpc_urls": {
           "testnet": "<testnet-rpc-url>",
           "mainnet": "<mainnet-rpc-url>"
       }
   }
   ```

5. **Build Contracts**
   ```bash
   make build
   ```

6. **Deploy Contracts**
   Use the `chain` flag to specify the target chain (default is `testnet`):
   ```bash
   make deploy chain=testnet
   ```
