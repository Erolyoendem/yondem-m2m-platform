from web3 import Web3
from eth_account import Account
import json
import os
from typing import Optional, Dict, Any

class YondemBlockchainClient:
    def __init__(self, provider_url: str, private_key: Optional[str] = None):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {provider_url}")
        
        self.account = None
        if private_key:
            self.account = Account.from_key(private_key)
        
        self.ydm_token = None
        self.publisher_contract = None
        self.platform_wallet = self.account.address if self.account else None
    
    def load_contract(self, address: str, abi: list):
        return self.w3.eth.contract(address=address, abi=abi)
    
    def deploy_yldm_token(self) -> str:
        if not self.account:
            raise ValueError("Private key required for deployment")
        
        bytecode = self._get_token_bytecode()
        abi = self._get_token_abi()
        
        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = Contract.constructor().build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 3000000,
            "gasPrice": self.w3.to_wei("20", "gwei")
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.ydm_token = self.load_contract(receipt.contractAddress, abi)
        return receipt.contractAddress
    
    def deploy_publisher_contract(self, token_address: str) -> str:
        if not self.account:
            raise ValueError("Private key required for deployment")
        
        bytecode = self._get_publisher_bytecode()
        abi = self._get_publisher_abi()
        
        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = Contract.constructor(token_address, self.platform_wallet).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 3000000,
            "gasPrice": self.w3.to_wei("20", "gwei")
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.publisher_contract = self.load_contract(receipt.contractAddress, abi)
        return receipt.contractAddress
    
    def create_deal(self, publisher: str, advertiser: str, product_id: int, amount: int, commission: int) -> int:
        if not self.publisher_contract:
            raise ValueError("Publisher contract not deployed")
        
        tx = self.publisher_contract.functions.createDeal(
            publisher, advertiser, product_id, amount, commission
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 300000,
            "gasPrice": self.w3.to_wei("20", "gwei")
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        logs = self.publisher_contract.events.DealCreated().process_receipt(receipt)
        return logs[0]["args"]["dealId"] if logs else 0
    
    def execute_deal(self, deal_id: int):
        if not self.publisher_contract:
            raise ValueError("Publisher contract not deployed")
        
        tx = self.publisher_contract.functions.executeDeal(deal_id).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 300000,
            "gasPrice": self.w3.to_wei("20", "gwei")
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    def get_balance(self, address: str) -> int:
        if not self.ydm_token:
            raise ValueError("YDM Token not deployed")
        return self.ydm_token.functions.balanceOf(address).call()
    
    def _get_token_abi(self) -> list:
        return json.loads(open("/Users/haksystems/Yondem-M2M-Platform/03-Implementation/mcp-server/blockchain/contracts/YDMToken.abi").read())
    
    def _get_token_bytecode(self) -> str:
        return open("/Users/haksystems/Yondem-M2M-Platform/03-Implementation/mcp-server/blockchain/contracts/YDMToken.bin").read()
    
    def _get_publisher_abi(self) -> list:
        return json.loads(open("/Users/haksystems/Yondem-M2M-Platform/03-Implementation/mcp-server/blockchain/contracts/PublisherContract.abi").read())
    
    def _get_publisher_bytecode(self) -> str:
        return open("/Users/haksystems/Yondem-M2M-Platform/03-Implementation/mcp-server/blockchain/contracts/PublisherContract.bin").read()
