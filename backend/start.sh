#!/bin/bash

# 환경 변수 로드
export $(cat .env | xargs)

# 데이터베이스 마이그레이션
cd backend
alembic upgrade head

# 백엔드 서버 실행
python main.py 2>&1 | tee -a server.log 