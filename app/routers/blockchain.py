from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import os
from app.blockchain import YondemBlockchainClient

router = APIRouter(prefix="/blockchain", tags=["blockchain"])

class DeployRequest(BaseModel):
    provider_url: str
    private_key: str

class DealRequest(BaseModel):
    publisher: str
    advertiser: str
    product_id: int
    amount: int
    commission: int

class ExecuteDealRequest(BaseModel):
    deal_id: int

@router.post("/deploy")
async def deploy_contracts(req: DeployRequest):
    try:
        client = YondemBlockchainClient(req.provider_url, req.private_key)
        token_addr = client.deploy_yldm_token()
        publisher_addr = client.deploy_publisher_contract(token_addr)
        return {
            "status": "success",
            "ydm_token": token_addr,
            "publisher_contract": publisher_addr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/deal")
async def create_deal(req: DealRequest):
    try:
        client = YondemBlockchainClient(
            os.getenv("BLOCKCHAIN_PROVIDER"),
            os.getenv("PLATFORM_PRIVATE_KEY")
        )
        deal_id = client.create_deal(
            req.publisher, req.advertiser,
            req.product_id, req.amount, req.commission
        )
        return {"deal_id": deal_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/deal/execute")
async def execute_deal(req: ExecuteDealRequest):
    try:
        client = YondemBlockchainClient(
            os.getenv("BLOCKCHAIN_PROVIDER"),
            os.getenv("PLATFORM_PRIVATE_KEY")
        )
        receipt = client.execute_deal(req.deal_id)
        return {"tx_hash": receipt.transactionHash.hex(), "status": "executed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/balance/{address}")
async def get_balance(address: str):
    try:
        client = YondemBlockchainClient(
            os.getenv("BLOCKCHAIN_PROVIDER"),
            os.getenv("PLATFORM_PRIVATE_KEY")
        )
        balance = client.get_balance(address)
        return {"address": address, "balance": str(balance)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
