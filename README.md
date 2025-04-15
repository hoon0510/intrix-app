# Intrix – AI 기반 욕구 분석 마케팅 전략 자동화 도구

Intrix는 AI를 활용하여 사용자 리뷰를 분석하고, 자동으로 마케팅 전략을 생성하는 도구입니다. GPT-4o와 Claude-3 API를 활용하여 감정 분석, 전략 수립, 카피라이팅, 브랜딩 전략을 자동화합니다.

## 🔧 기술 스택

### 백엔드
- FastAPI (Python)
- OpenAI GPT-4o API
- Anthropic Claude-3 API
- PostgreSQL (Railway)
- WeasyPrint (PDF 생성)

### 프론트엔드
- Next.js 14
- TypeScript
- Tailwind CSS
- NextAuth.js (인증)

### 배포
- Railway (백엔드)
- Vercel (프론트엔드)

## 📦 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/your-org/intrix-app.git
cd intrix-app
```

2. 백엔드 의존성 설치
```bash
# Python 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

3. 프론트엔드 의존성 설치
```bash
cd frontend
npm install
```

## ⚙️ 실행 방법

1. 환경 변수 설정
```bash
# .env.example 파일을 복사하여 .env 파일 생성
cp .env.example .env
```

2. 백엔드 실행
```bash
# 개발 모드
uvicorn api.main:app --reload

# 프로덕션 모드
uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

3. 프론트엔드 실행
```bash
cd frontend
npm run dev
```

## 🔑 환경 변수 설정

`.env` 파일에 다음 환경 변수들을 설정해야 합니다:

```env
# API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-claude-api-key

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Database
RAILWAY_DB_URL=your-railway-db-url

# Environment Settings
ENV=production
LOGIN_REQUIRED=true
PORT=8000

# Frontend Settings
NEXT_PUBLIC_BACKEND_URL=https://your-railway-backend-url
NEXT_PUBLIC_APP_URL=https://your-vercel-frontend-url
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=your-stripe-public-key
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

## 🚀 배포 가이드

### Railway (백엔드)
1. Railway 계정 생성 및 로그인
2. 새 프로젝트 생성
3. GitHub 저장소 연결
4. 환경 변수 설정
5. 배포 시작

### Vercel (프론트엔드)
1. Vercel 계정 생성 및 로그인
2. 새 프로젝트 생성
3. GitHub 저장소 연결
4. 환경 변수 설정
5. 배포 시작

## 📁 주요 기능

### 1. 리뷰 분석
- 감정 분석
- 욕구 분석
- 키워드 추출

### 2. 전략 생성
- 마케팅 전략
- 브랜딩 전략
- 실행 전략

### 3. 카피라이팅
- 브랜드 카피
- 광고 카피
- SNS 카피

### 4. 보고서 생성
- HTML 보고서
- PDF 다운로드
- 공유 링크 생성

### 5. 사용자 관리
- 마이페이지
- 분석 이력
- 즐겨찾기

## 📝 API 문서

API 문서는 다음 URL에서 확인할 수 있습니다:
- 개발 환경: `http://localhost:8000/docs`
- 프로덕션 환경: `https://your-railway-backend-url/docs`

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
