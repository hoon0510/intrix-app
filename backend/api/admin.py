from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas.user import UserResponse
from ..models.user import User
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def list_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@router.patch("/users/{user_id}/credit")
async def update_user_credit(
    user_id: str,
    credit_update: dict,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if "amount" not in credit_update:
            raise HTTPException(status_code=400, detail="Credit amount is required")
            
        new_credit = user.credit + credit_update["amount"]
        if new_credit < 0:
            raise HTTPException(status_code=400, detail="Credit cannot be negative")
            
        user.credit = new_credit
        db.commit()
        return {"message": "Credit updated successfully", "new_credit": new_credit}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update credit: {str(e)}") 