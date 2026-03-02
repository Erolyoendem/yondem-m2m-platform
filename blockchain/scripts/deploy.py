#!/usr/bin/env python3
import os
import sys
sys.path.append("/Users/haksystems/Yondem-M2M-Platform/03-Implementation/mcp-server")

from app.blockchain.web3_client import YondemBlockchainClient

def main():
    provider = os.getenv("BLOCKCHAIN_PROVIDER", "https://polygon-mumbai.g.alchemy.com/v2/YOUR_KEY")
    private_key = os.getenv("PLATFORM_PRIVATE_KEY")
    
    if not private_key:
        print("❌ PLATFORM_PRIVATE_KEY not set")
        return
    
    print("🚀 Starting deployment...")
    client = YondemBlockchainClient(provider, private_key)
    
    print("📄 Deploying YDM Token...")
    token_address = client.deploy_yldm_token()
    print(f"✅ YDM Token deployed at: {token_address}")
    
    print("📄 Deploying Publisher Contract...")
    publisher_address = client.deploy_publisher_contract(token_address)
    print(f"✅ Publisher Contract deployed at: {publisher_address}")
    
    print("\\n📝 Update .env with:")
    print(f"YDM_TOKEN_ADDRESS={token_address}")
    print(f"PUBLISHER_CONTRACT_ADDRESS={publisher_address}")

if __name__ == "__main__":
    main()
