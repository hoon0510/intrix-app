from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.user import UserResponse
from services.user_service import get_all_users, update_user_credit

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users():
    try:
        users = await get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/users/{user_id}/credit")
async def update_credit(user_id: int, credit_update: dict):
    try:
        if "credit" not in credit_update:
            raise HTTPException(status_code=400, detail="Credit amount is required")
        
        credit = credit_update["credit"]
        if credit < 0:
            raise HTTPException(status_code=400, detail="Credit cannot be negative")
        
        await update_user_credit(user_id, credit)
        return {"message": f"User {user_id} credit updated to {credit}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 