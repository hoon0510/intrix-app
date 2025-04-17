from typing import List
from models.user import User
from database import get_db
from sqlalchemy.orm import Session

async def get_all_users() -> List[User]:
    """
    모든 사용자 정보를 조회합니다.
    
    Returns:
        List[User]: 사용자 목록
    """
    db = next(get_db())
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()

async def update_user_credit(user_id: int, credit: int) -> None:
    """
    사용자의 크레딧을 업데이트합니다.
    
    Args:
        user_id (int): 사용자 ID
        credit (int): 새로운 크레딧 값
    """
    db = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        user.credit = credit
        db.commit()
    finally:
        db.close() 