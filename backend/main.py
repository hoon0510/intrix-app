import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router
from dotenv import load_dotenv
from models.user import Base
from database import engine

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(
    title="Intrix API",
    description="AI-powered brand strategy analysis API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 