from fastapi import Header, HTTPException

async def get_current_user_id(x_user_id: str = Header(...)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")
    return x_user_id 