"""
Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException, Header, Depends, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import uuid
import os
from dotenv import load_dotenv
import zipfile
from io import BytesIO
import time
import json
import logging

from api.services.analyzer_claude import Analyzer
from api.services.strategist import Strategist
from api.services.copywriter import Copywriter
from api.services.formatter_claude import Formatter
from api.services.credit_manager import CreditManager
from api.crawlers.dispatcher import CrawlerDispatcher
from api.utils.auth import verify_auth_token
from api.services.analysis_history import AnalysisHistory
from weasyprint import HTML
from api.services.brand_strategy import BrandStrategyGenerator
from api.endpoints import analysis, strategy, copy, formatting, credit, download
from api.routes import crawler, auth, share, feedback, history, favorite, export, execution, admin, credit_log
from api.services.favorite_manager import (
    add_favorite,
    remove_favorite,
    get_favorites,
    is_favorited
)
from api.services.zip_download_limiter import (
    is_download_allowed,
    record_download_time,
    get_remaining_cooldown
)
from api.services.feedback_manager import add_feedback, get_feedback_summary, submit_feedback
from api.services.scheduler_manager import schedule_analysis
from api.services.api_key_manager import generate_api_key, create_api_key, is_valid_api_key, get_user_by_api_key, get_api_key_by_user
from api.services.gpt_caller import GPTCaller
from api.services.claude_caller import ClaudeCaller
from api.crawlers.reddit_scraper import RedditScraper
from api.handlers.exception_handler import register_exception_handlers
from api.middleware.logger import LoggingMiddleware
from api.config.logging_config import configure_logging
from api.db.database import engine
from api.models import base
from api.middleware.exception_handler import exception_handler
from api.middleware.error_handler import global_error_handler

# Load environment variables from .env file
load_dotenv()

# Environment variables with defaults
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LOGIN_REQUIRED = os.getenv("LOGIN_REQUIRED", "false").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))

# Mock data storage for analysis results
mock_analysis_storage = {
    "1": {
        "date": "2024-03-15T10:30:00",
        "channels": ["community", "sns"],
        "copy": "당신의 브랜드 이야기를 전 세계에 알리세요",
        "strategy_summary": "글로벌 시장 진출을 위한 종합 마케팅 전략",
        "report_html": "<div>...</div>",
        "style": "감성적"
    },
    "2": {
        "date": "2024-03-16T14:45:00",
        "channels": ["sns"],
        "copy": "더 나은 미래를 위한 첫 걸음",
        "strategy_summary": "지속가능한 브랜드 이미지 구축 전략",
        "report_html": "<div>...</div>",
        "style": "감성적"
    }
}

# Mock data storage for brand history
mock_brand_history = {
    "user1": [
        {
            "id": "1",
            "created_at": "2024-03-15T10:30:00",
            "reference_point": "갤럭시 S 시리즈",
            "frame_shift": "AI 기능을 강조한 업무 최적화 기기",
            "positioning": "생각보다 빠른, 일보다 똑똑한"
        },
        {
            "id": "2",
            "created_at": "2024-03-16T14:20:00",
            "reference_point": "애플 워치",
            "frame_shift": "건강 관리 중심의 라이프스타일 기기",
            "positioning": "건강한 삶의 시작, 당신의 손목에서"
        }
    ],
    "user2": [
        {
            "id": "3",
            "created_at": "2024-03-17T09:15:00",
            "reference_point": "테슬라 모델 3",
            "frame_shift": "지속가능한 이동성의 새로운 기준",
            "positioning": "미래를 향한 첫 걸음"
        }
    ]
}

# Mock data for brand strategy
mock_brand_strategy_storage = {
    "1": {
        "reference_point": "글로벌 시장의 선두주자",
        "frame_shift": "지역적 한계를 넘어선 글로벌 브랜드",
        "positioning": "세계를 연결하는 혁신적인 플랫폼"
    },
    "2": {
        "reference_point": "지속가능한 미래의 아이콘",
        "frame_shift": "일회성에서 지속가능성으로의 전환",
        "positioning": "미래 세대를 위한 지속가능한 솔루션"
    }
}

# Share link storage
share_link_storage: Dict[str, Dict[str, str]] = {}

# Mock data storage for favorites
mock_favorites_storage: Dict[str, List[str]] = {}

# Initialize services
analyzer = Analyzer()
strategist = Strategist()
copywriter = Copywriter()
formatter = Formatter()
credit_manager = CreditManager()
crawler_dispatcher = CrawlerDispatcher()
analysis_history = AnalysisHistory()
brand_strategy_generator = BrandStrategyGenerator()

# 로그 디렉토리 생성
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 로깅 설정 적용
logger = configure_logging()

# 데이터베이스 테이블 생성
base.Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="Intrix API",
    description="API for Intrix Analysis Platform",
    version="1.0.0"
)

# 예외 핸들러 등록
register_exception_handlers(app)

# 로깅 미들웨어 등록
app.add_middleware(LoggingMiddleware)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 로그인 필수 미들웨어
@app.middleware("http")
async def check_login_required(request: Request, call_next):
    # 로그인 필수 설정이 켜져있고, 인증이 필요한 경로인 경우
    if LOGIN_REQUIRED and not request.url.path.startswith("/auth"):
        # Authorization 헤더 확인
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
    
    response = await call_next(request)
    return response

# 라우터 등록
app.include_router(crawler.router, prefix="/api", tags=["crawler"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(share.router, prefix="/api", tags=["share"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(favorite.router, prefix="/api", tags=["favorite"])
app.include_router(export.router, prefix="/api", tags=["export"])
app.include_router(execution.router, prefix="/api", tags=["execution"])
app.include_router(admin.router, prefix="/api", tags=["admin"])
app.include_router(credit_log.router, prefix="/api", tags=["credit"])
app.include_router(analysis.router, prefix="/api")
app.include_router(download.router, prefix="/api")

# Request models
class AnalyzeRequest(BaseModel):
    text: str
    user_id: str

class StrategyRequest(BaseModel):
    analysis_result: Dict
    user_id: str
    prompt_type: Optional[str] = "existing"

class CopyRequest(BaseModel):
    strategy: Dict
    analysis_result: Dict
    user_id: str
    style: Optional[str] = None

class FormatRequest(BaseModel):
    strategy: Dict
    analysis: Dict
    copy: Dict
    user_id: str
    output_format: Optional[str] = "html"

class CreditRequest(BaseModel):
    text: str
    community_channels: List[str]
    sns_channels: List[str]
    user_id: str

class FullAnalysisRequest(BaseModel):
    input_text: str
    channels: List[str]

class ABTestRequest(BaseModel):
    input_text: str
    channels: List[str]
    variant_count: int = Field(ge=2, le=5, description="Number of variants to generate (2-5)")

class BrandStrategyRequest(BaseModel):
    strategy: Dict

class ShareLinkRequest(BaseModel):
    """Request model for generating share links."""
    user_id: str
    analysis_id: str

class ShareLinkResponse(BaseModel):
    """Response model for share link generation."""
    share_url: str

class FeedbackRequest(BaseModel):
    user_id: str
    analysis_id: str
    feedback: str

class FeedbackResponse(BaseModel):
    message: str

class FeedbackSummaryResponse(BaseModel):
    positive: int
    negative: int

class ScheduleAnalysisRequest(BaseModel):
    user_id: str
    input_text: str
    channels: List[str]
    frequency: str

class ScheduleAnalysisResponse(BaseModel):
    message: str

class ApiKeyRegisterRequest(BaseModel):
    user_id: str

class ApiKeyRegisterResponse(BaseModel):
    api_key: str

class ApiAccessStrategyRequest(BaseModel):
    input_text: str
    channels: List[str]

class ApiAccessStrategyResponse(BaseModel):
    copy: str
    style: str
    report_html: str

class TestAnalysisRequest(BaseModel):
    keyword: str

class TestAnalysisResponse(BaseModel):
    analysis: Dict[str, Any]
    strategy: Dict[str, Any]
    formatted: Dict[str, Any]

# Rate limiting cache for ZIP downloads
zip_download_cache: Dict[str, float] = {}
ZIP_DOWNLOAD_COOLDOWN = 600  # 10 minutes in seconds

# API endpoints
@app.post("/analyze")
async def analyze_text(request: AnalyzeRequest):
    """
    Analyze text for sentiment and desires
    """
    try:
        result = await analyzer.analyze_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/strategy")
async def generate_strategy(request: StrategyRequest):
    """
    Generate marketing strategy based on analysis
    """
    try:
        result = strategist.generate_strategy(
            request.analysis_result,
            request.prompt_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/copy")
async def generate_copy(request: CopyRequest):
    """
    Generate marketing copy based on strategy and analysis
    """
    try:
        result = copywriter.generate_copy(
            request.strategy,
            request.analysis_result,
            request.style
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/format")
async def format_report(request: FormatRequest):
    """
    Format the final report
    """
    try:
        result = formatter.format_report(
            request.strategy,
            request.analysis,
            request.copy
        )
        
        if request.output_format == "html":
            output = formatter.generate_html(result)
            return {"format": "html", "content": output}
        else:
            return {"format": "json", "content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/full_analysis")
async def full_analysis(
    request: Dict,
    auth_token: Optional[str] = Header(None)
):
    """
    Full analysis endpoint that requires authentication
    """
    # Verify authentication
    user_id, is_authenticated = verify_auth_token(auth_token)
    if not is_authenticated:
        raise HTTPException(status_code=403, detail="Authentication required")

    input_text = request.get("input_text")
    channels = request.get("channels", [])
    
    try:
        # Run analysis pipeline
        crawl_results = await crawler_dispatcher.run_selected_crawlers(channels)
        analysis_result = await analyzer.analyze_text(input_text)
        strategy = await strategist.generate_strategy(analysis_result)
        copy = await copywriter.generate_copy(strategy, analysis_result)
        report = await formatter.format_strategy(strategy, analysis_result, copy)
        
        # Calculate and check credits
        credit_info = credit_manager.process_request(
            text=input_text,
            community_channels=[],  # Add actual channel categorization
            sns_channels=[],  # Add actual channel categorization
            user_id=user_id,
            ip_address=None  # Not needed for authenticated requests
        )
        
        return {
            "final_credit": credit_info["final_credit"],
            "from_cache": credit_info["from_cache"],
            "free_trial": credit_info["free_trial"],
            "copy": copy,
            "report_html": report["html"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ab-test")
async def ab_test(
    request: ABTestRequest,
    auth_token: Optional[str] = Header(None)
):
    """
    Generate multiple variants of analysis and copy for A/B testing
    
    Args:
        request: ABTestRequest containing input text, channels, and variant count
        auth_token: Authentication token
        
    Returns:
        Dictionary containing variants, final credit, and cache status
    """
    # Verify authentication
    user_id, is_authenticated = verify_auth_token(auth_token)
    if not is_authenticated:
        raise HTTPException(status_code=403, detail="Authentication required")
    
    try:
        # Calculate required credits with variant multiplier
        base_credit = credit_manager.calculate_base_credits(request.input_text)
        channel_credit = credit_manager.calculate_channel_credits(request.channels)
        total_credit = (base_credit + channel_credit) * request.variant_count
        
        # Check if user has enough credits
        if not credit_manager.check_credits(user_id, total_credit):
            raise HTTPException(
                status_code=402,
                detail=f"Insufficient credits. Required: {total_credit}"
            )
        
        variants = []
        for i in range(request.variant_count):
            # Run crawlers
            crawl_results = await crawler_dispatcher.run_selected_crawlers(request.channels)
            
            # Analyze text
            analysis_result = await analyzer.analyze_text(request.input_text)
            
            # Generate strategy
            strategy = await strategist.generate_strategy(analysis_result)
            
            # Generate copy
            copy = await copywriter.generate_copy(strategy, analysis_result)
            
            # Format report
            report = await formatter.format_report(strategy, analysis_result, copy)
            
            # Add to variants
            variants.append({
                "variant_id": f"variant_{i+1}",
                "analysis": analysis_result,
                "strategy": strategy,
                "copy": copy,
                "report_html": report
            })
        
        # Deduct credits
        credit_manager.deduct_credits(user_id, total_credit)
        
        return {
            "variants": variants,
            "final_credit": total_credit,
            "from_cache": False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/brand-strategy")
async def generate_brand_strategy(
    request: BrandStrategyRequest,
    auth_token: Optional[str] = Header(None)
):
    """
    Generate brand strategy elements from GPT strategy results.
    
    Args:
        request: BrandStrategyRequest containing GPT strategy
        auth_token: Authentication token
        
    Returns:
        Dictionary containing brand strategy elements:
        {
            "reference_point": "...",
            "frame_shift": "...",
            "positioning": "..."
        }
    """
    # Verify authentication
    user_id, is_authenticated = verify_auth_token(auth_token)
    if not is_authenticated:
        raise HTTPException(status_code=403, detail="Authentication required")
    
    try:
        # Generate brand strategy elements
        brand_strategy = brand_strategy_generator.generate(request.strategy)
        
        return brand_strategy
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Intrix API"}

@app.get("/get-analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Retrieve analysis results by ID
    """
    try:
        if analysis_id not in mock_analysis_storage:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return mock_analysis_storage[analysis_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "operational"
    }

@app.get("/user/{user_id}/history")
async def get_user_history(
    user_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Get analysis history for a user
    
    Args:
        user_id: ID of the user
        auth_token: Authentication token
        
    Returns:
        List of analysis records for the user
    """
    # Verify authentication
    auth_user_id, is_authenticated = verify_auth_token(auth_token)
    if not is_authenticated or auth_user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    try:
        history = analysis_history.get_user_history(user_id)
        return {
            "status": "success",
            "data": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}/download/{analysis_id}")
async def download_analysis_pdf(
    user_id: str,
    analysis_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Download analysis result as PDF
    
    Args:
        user_id: ID of the user
        analysis_id: ID of the analysis
        auth_token: Authentication token
        
    Returns:
        PDF file as response
    """
    # Verify authentication
    auth_user_id, is_authenticated = verify_auth_token(auth_token)
    if not is_authenticated or auth_user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    try:
        # Get analysis result
        analysis = analysis_history.get_analysis_by_id(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        if analysis.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized access")
            
        # Get HTML content
        html_content = analysis.get("result", {}).get("report_html")
        if not html_content:
            raise HTTPException(status_code=404, detail="Report HTML not found")
            
        # Convert HTML to PDF
        pdf = HTML(string=html_content).write_pdf()
        
        # Create response
        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="analysis_{analysis_id}.pdf"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}/brand-history")
async def get_brand_history(
    user_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Get brand strategy history for a specific user.
    
    Args:
        user_id: ID of the user
        auth_token: Authentication token
        
    Returns:
        List of brand strategy history items
    """
    # Verify authentication
    current_user_id, is_authenticated = verify_auth_token(auth_token)
    if not is_authenticated:
        raise HTTPException(status_code=403, detail="Authentication required")
    
    # Verify user access
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        # Get user's brand history from mock data
        history = mock_brand_history.get(user_id, [])
        
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}/brand/{strategy_id}")
async def get_brand_strategy(
    user_id: str,
    strategy_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Get a specific brand strategy by ID.
    
    Args:
        user_id: ID of the user
        strategy_id: ID of the brand strategy
        auth_token: Authentication token
        
    Returns:
        Brand strategy details including reference_point, frame_shift, and positioning
    """
    # Verify authentication
    current_user_id, is_authenticated = verify_auth_token(auth_token)
    if not is_authenticated:
        raise HTTPException(status_code=403, detail="Authentication required")
    
    # Verify user access
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        # Get user's brand history
        history = mock_brand_history.get(user_id, [])
        
        # Find strategy by ID
        strategy = next((item for item in history if item["id"] == strategy_id), None)
        
        if not strategy:
            raise HTTPException(status_code=404, detail="Brand strategy not found")
        
        return {
            "reference_point": strategy["reference_point"],
            "frame_shift": strategy["frame_shift"],
            "positioning": strategy["positioning"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Share endpoints
@app.post("/share-link", response_model=Dict[str, str])
async def create_share_link(request: ShareLinkRequest):
    try:
        # Get user ID from token
        user_id = get_user_id_from_token(request.token)
        if not user_id:
            raise HTTPException(status_code=403, detail="인증되지 않은 사용자입니다")

        # Generate or get existing share link
        share_uuid = create_share_link(user_id, request.analysis_id)
        if not share_uuid:
            raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다")

        # Construct share URL
        base_url = os.getenv("BASE_URL", "http://localhost:3000")
        share_url = f"{base_url}/share/{share_uuid}"

        return {"share_url": share_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/share/{share_uuid}", response_model=Dict[str, Any])
async def get_shared_analysis(share_uuid: str):
    try:
        # Get analysis ID from share UUID with production TTL
        analysis_id = get_analysis_id_by_uuid(share_uuid, ttl=PRODUCTION_TTL)
        if not analysis_id:
            raise HTTPException(status_code=404, detail="공유 링크가 만료되었습니다")

        # Get analysis data
        analysis = get_analysis_by_id(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="공유 링크가 만료되었습니다")

        # Get brand strategy data
        brand_strategy = get_brand_strategy_by_id(analysis_id)
        if not brand_strategy:
            raise HTTPException(status_code=404, detail="공유 링크가 만료되었습니다")

        return {
            "positioning": brand_strategy.get("positioning", ""),
            "copy": analysis.get("copy", ""),
            "style": analysis.get("style", ""),
            "report_html": analysis.get("report_html", "")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/share/{share_uuid}", response_model=Dict[str, str])
async def delete_share_link(share_uuid: str):
    """
    Delete a share link.
    
    Args:
        share_uuid: UUID of the share link to delete
        
    Returns:
        Dict containing success message
    """
    try:
        # Delete the share link
        delete_share_link(share_uuid)
        
        return {"message": "공유 링크가 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/share-link/existence", response_model=Dict[str, bool])
async def check_share_link_existence(user_id: str, analysis_id: str):
    """
    Check if a share link exists for the given user and analysis.
    
    Args:
        user_id: ID of the user
        analysis_id: ID of the analysis
        
    Returns:
        Dict containing existence status
    """
    try:
        exists = exists_share_link(user_id, analysis_id)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/favorite/{analysis_id}")
async def add_favorite(
    analysis_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Add an analysis to favorites.
    
    Args:
        analysis_id: The ID of the analysis to favorite
        auth_token: Authentication token from header
        
    Returns:
        Dict with status message
        
    Raises:
        HTTPException: If authentication fails or analysis not found
    """
    try:
        # Verify authentication
        user_id = verify_auth_token(auth_token)
        if not user_id:
            raise HTTPException(status_code=403, detail="Authentication failed")
            
        # Check if analysis exists
        if analysis_id not in mock_analysis_storage:
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        # Initialize user's favorites if not exists
        if user_id not in mock_favorites_storage:
            mock_favorites_storage[user_id] = []
            
        # Add to favorites if not already favorited
        if analysis_id not in mock_favorites_storage[user_id]:
            mock_favorites_storage[user_id].append(analysis_id)
            
        return {"status": "favorited"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/favorite/{analysis_id}")
async def remove_favorite(
    analysis_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Remove an analysis from favorites.
    
    Args:
        analysis_id: The ID of the analysis to unfavorite
        auth_token: Authentication token from header
        
    Returns:
        Dict with status message
        
    Raises:
        HTTPException: If authentication fails or analysis not found
    """
    try:
        # Verify authentication
        user_id = verify_auth_token(auth_token)
        if not user_id:
            raise HTTPException(status_code=403, detail="Authentication failed")
            
        # Check if analysis exists
        if analysis_id not in mock_analysis_storage:
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        # Remove from favorites if exists
        if user_id in mock_favorites_storage and analysis_id in mock_favorites_storage[user_id]:
            mock_favorites_storage[user_id].remove(analysis_id)
            
        return {"status": "unfavorited"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/favorites/{user_id}")
async def get_user_favorites(
    user_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Get list of favorited analysis IDs for a user.
    
    Args:
        user_id: ID of the user
        auth_token: Authentication token from header
        
    Returns:
        Dict with list of favorited analysis IDs
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Verify authentication
        verified_user_id = verify_auth_token(auth_token)
        if not verified_user_id or verified_user_id != user_id:
            raise HTTPException(status_code=403, detail="Authentication failed")
            
        # Get favorites
        favorites = get_favorites(user_id)
        
        return {"favorites": favorites}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/favorite/status")
async def check_favorite_status(
    user_id: str,
    analysis_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Check if an analysis is favorited by a user.
    
    Args:
        user_id: ID of the user
        analysis_id: ID of the analysis to check
        auth_token: Authentication token from header
        
    Returns:
        Dict with favorited status
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Verify authentication
        verified_user_id = verify_auth_token(auth_token)
        if not verified_user_id or verified_user_id != user_id:
            raise HTTPException(status_code=403, detail="Authentication failed")
            
        # Check favorite status
        favorited = is_favorited(user_id, analysis_id)
        
        return {"favorited": favorited}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/download/favorites")
async def download_favorite_reports(
    user_id: str,
    auth_token: Optional[str] = Header(None)
):
    """
    Download all favorited reports as a ZIP file.
    
    Args:
        user_id: The ID of the user requesting the download
        auth_token: Optional authentication token
        
    Returns:
        ZIP file containing all favorited reports as PDFs
        
    Raises:
        HTTPException: If authentication fails, no favorites found, or rate limit exceeded
    """
    try:
        # Verify authentication
        if auth_token:
            if not verify_auth_token(auth_token):
                raise HTTPException(status_code=403, detail="Invalid authentication token")
        
        # Check rate limit
        if not is_download_allowed(user_id):
            remaining = get_remaining_cooldown(user_id)
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "ZIP 파일 다운로드는 10분에 1회만 가능합니다.",
                    "remaining_seconds": remaining
                }
            )
        
        # Get list of favorited analysis IDs
        favorite_ids = get_favorites(user_id)
        if not favorite_ids:
            raise HTTPException(status_code=404, detail="No favorited reports found")
        
        # Create in-memory ZIP file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for analysis_id in favorite_ids:
                try:
                    # Get analysis data
                    analysis = mock_analysis_storage.get(analysis_id)
                    if not analysis:
                        continue
                        
                    # Get brand strategy data
                    brand_strategy = mock_brand_strategy_storage.get(analysis_id, {})
                    
                    # Combine HTML content
                    html_content = f"""
                    <html>
                        <head>
                            <meta charset="UTF-8">
                            <style>
                                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                                .copy {{ font-size: 24px; margin-bottom: 20px; }}
                                .branding {{ margin-top: 20px; padding: 10px; background: #f5f5f5; }}
                            </style>
                        </head>
                        <body>
                            <div class="copy">{analysis['copy']}</div>
                            {analysis['report_html']}
                            <div class="branding">
                                <h3>브랜드 전략</h3>
                                <p>참조점: {brand_strategy.get('reference_point', 'N/A')}</p>
                                <p>프레임 시프트: {brand_strategy.get('frame_shift', 'N/A')}</p>
                                <p>포지셔닝: {brand_strategy.get('positioning', 'N/A')}</p>
                            </div>
                        </body>
                    </html>
                    """
                    
                    # Generate PDF
                    pdf_buffer = BytesIO()
                    HTML(string=html_content).write_pdf(pdf_buffer)
                    
                    # Add PDF to ZIP
                    zip_file.writestr(f"strategy_{analysis_id}.pdf", pdf_buffer.getvalue())
                    
                except Exception as e:
                    print(f"Error processing analysis {analysis_id}: {str(e)}")
                    continue
        
        # Record successful download
        record_download_time(user_id)
        
        # Prepare response
        zip_buffer.seek(0)
        return Response(
            content=zip_buffer.getvalue(),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=favorite_reports_{user_id}.zip"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate ZIP file: {str(e)}")

@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit feedback for an analysis.
    
    Args:
        feedback: FeedbackRequest containing user_id, analysis_id, and feedback type
    
    Returns:
        FeedbackResponse with success message
    
    Raises:
        HTTPException: If feedback is invalid or submission fails
    """
    try:
        add_feedback(
            user_id=feedback.user_id,
            analysis_id=feedback.analysis_id,
            feedback=feedback.feedback
        )
        return FeedbackResponse(message="피드백이 저장되었습니다.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="피드백 저장 중 오류가 발생했습니다")

@app.get("/feedback/summary/{analysis_id}", response_model=FeedbackSummaryResponse)
async def get_feedback_summary_endpoint(analysis_id: str):
    """
    Get summary of feedback for an analysis.
    
    Args:
        analysis_id: ID of the analysis
    
    Returns:
        FeedbackSummaryResponse with counts of positive and negative feedback
    
    Raises:
        HTTPException: If there's an error retrieving the summary
    """
    try:
        summary = get_feedback_summary(analysis_id)
        return FeedbackSummaryResponse(**summary)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="피드백 요약을 가져오는 중 오류가 발생했습니다"
        )

@app.post("/schedule-analysis", response_model=ScheduleAnalysisResponse)
async def schedule_analysis_endpoint(request: ScheduleAnalysisRequest):
    """
    Schedule a new analysis task.
    
    Args:
        request: ScheduleAnalysisRequest containing scheduling details
    
    Returns:
        ScheduleAnalysisResponse with success message
    
    Raises:
        HTTPException: If scheduling fails
    """
    try:
        schedule_analysis(
            user_id=request.user_id,
            input_text=request.input_text,
            channels=request.channels,
            frequency=request.frequency
        )
        return ScheduleAnalysisResponse(message="분석이 예약되었습니다.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="분석 예약 중 오류가 발생했습니다"
        )

@app.post("/api-access/register", response_model=ApiKeyRegisterResponse)
async def register_api_key(request: ApiKeyRegisterRequest):
    """
    Register a new API key for a user.
    
    Args:
        request: ApiKeyRegisterRequest containing user_id
    
    Returns:
        ApiKeyRegisterResponse with generated API key
    
    Raises:
        HTTPException: If registration fails
    """
    try:
        api_key = generate_api_key(request.user_id)
        return ApiKeyRegisterResponse(api_key=api_key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="API 키 등록 중 오류가 발생했습니다"
        )

@app.post("/api-access/strategy", response_model=ApiAccessStrategyResponse)
async def api_access_strategy(
    request: ApiAccessStrategyRequest,
    api_key: str = Header(..., alias="API-Key")
):
    """
    Generate strategy using API key authentication.
    
    Args:
        request: ApiAccessStrategyRequest containing input_text and channels
        api_key: API key from header
    
    Returns:
        ApiAccessStrategyResponse with strategy results
    
    Raises:
        HTTPException: If API key is invalid or strategy generation fails
    """
    try:
        # Validate API key
        user_id = get_user_id(api_key)
        if not user_id:
            raise HTTPException(
                status_code=403,
                detail="유효하지 않은 API 키입니다"
            )
        
        # Run crawlers
        crawl_results = await crawler_dispatcher.run_selected_crawlers(request.channels)
        
        # Analyze text
        analysis_result = await analyzer.analyze_text(request.input_text)
        
        # Generate strategy
        strategy = await strategist.generate_strategy(analysis_result)
        
        # Generate copy
        copy = await copywriter.generate_copy(strategy, analysis_result)
        
        # Format report
        report = await formatter.format_report(strategy, analysis_result, copy)
        
        return ApiAccessStrategyResponse(
            copy=copy,
            style=analysis_result.get("style", "감성적"),
            report_html=report["html"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="전략 생성 중 오류가 발생했습니다"
        )

@app.post("/test-analysis", response_model=TestAnalysisResponse)
async def test_analysis(request: TestAnalysisRequest):
    try:
        # Initialize services
        scraper = RedditScraper()
        claude = ClaudeCaller()
        gpt = GPTCaller()
        
        # 1. Scrape Reddit
        scraped_texts = await scraper.scrape(request.keyword)
        combined_text = "\n\n".join(scraped_texts)
        
        # 2. Analyze with Claude
        analysis_prompt = f"""
        Analyze the following Reddit posts about {request.keyword}:
        {combined_text}
        
        Provide insights about:
        1. Main topics discussed
        2. Sentiment analysis
        3. Key points and arguments
        4. Potential opportunities
        """
        
        analysis_result = await claude.call(
            prompt=analysis_prompt,
            system="You are an expert analyst specializing in social media content analysis."
        )
        
        # 3. Generate strategy with GPT
        strategy_prompt = f"""
        Based on the following analysis of {request.keyword}:
        {analysis_result['content']}
        
        Create a marketing strategy that includes:
        1. Target audience
        2. Key messages
        3. Channel recommendations
        4. Implementation timeline
        """
        
        strategy_result = await gpt.call(
            prompt=strategy_prompt,
            system="You are a marketing strategy expert."
        )
        
        # 4. Format with Claude
        format_prompt = f"""
        Format the following strategy into a clear, structured report:
        {strategy_result['content']}
        
        Include:
        1. Executive summary
        2. Detailed recommendations
        3. Action items
        4. Success metrics
        """
        
        formatted_result = await claude.call(
            prompt=format_prompt,
            system="You are a professional report formatter."
        )
        
        return TestAnalysisResponse(
            analysis=json.loads(analysis_result['content']),
            strategy=json.loads(strategy_result['content']),
            formatted=json.loads(formatted_result['content'])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Intrix API",
        version="1.0.0",
        description="Intrix API Documentation",
        routes=app.routes,
    )
    
    # Add example for crawl endpoint
    openapi_schema["paths"]["/api/crawl"]["post"]["requestBody"] = {
        "content": {
            "application/json": {
                "example": {
                    "user_id": "u001",
                    "input_text": "청년 정치의 방향성",
                    "channels": ["reddit", "dcinside"]
                }
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Register global error handler
@app.exception_handler(Exception)
async def catch_all_exceptions(request: Request, exc: Exception):
    return await global_error_handler(request, exc)
