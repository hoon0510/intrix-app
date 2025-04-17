#!/bin/bash

# 환경 변수 로드
export $(cat .env | xargs)

# 백엔드 서버 실행
cd backend
python main.py 2>&1 | tee -a server.log 