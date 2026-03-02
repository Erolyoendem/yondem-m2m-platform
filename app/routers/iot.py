from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
import uuid

from app.database.session import get_db
from app.models.iot_device import IoTDevice
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/iot", tags=["IoT Gateway"])

class DeviceRegister(BaseModel):
    name: str
    device_type: str

@router.post("/devices/register")
@limiter.limit("5/minute")
async def register_device(
    request: Request,
    data: DeviceRegister,
    db: Session = Depends(get_db)
):
    """Register a new IoT device
    
    - **name**: Device name (e.g., "Kitchen Fridge")
    - **device_type**: Type (fridge, printer, sensor, etc.)
    - Returns API key for device authentication
    """
    device_id = str(uuid.uuid4())
    api_key = str(uuid.uuid4())
    
    device = IoTDevice(
        id=device_id,
        name=data.name,
        device_type=data.device_type,
        api_key=api_key
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    
    return {
        "status": "success",
        "device_id": device_id,
        "api_key": api_key,
        "message": "Device registered successfully"
    }

@router.get("/devices/{device_id}/status")
@limiter.limit("60/minute")
async def get_device_status(
    request: Request,
    device_id: str,
    db: Session = Depends(get_db)
):
    """Get status of a specific IoT device
    """
    device = db.query(IoTDevice).filter(IoTDevice.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {
        "status": "success",
        "device": {
            "id": device.id,
            "name": device.name,
            "type": device.device_type,
            "status": device.status,
            "auto_order": device.auto_order_enabled,
            "budget_limit": device.budget_limit
        }
    }

@router.get("/devices")
@limiter.limit("30/minute")
async def list_devices(
    request: Request,
    db: Session = Depends(get_db)
):
    """List all registered IoT devices
    """
    devices = db.query(IoTDevice).all()
    return {
        "status": "success",
        "count": len(devices),
        "devices": [{"id": d.id, "name": d.name, "type": d.device_type, "status": d.status} for d in devices]
    }
