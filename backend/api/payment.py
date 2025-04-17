from fastapi import APIRouter, Request, HTTPException
import stripe
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def credit_to_price(credit: int) -> int:
    """크레딧 수량을 가격으로 변환"""
    price_map = {
        500: 499,    # $4.99
        2000: 2199,  # $21.99
        10000: 8999  # $89.99
    }
    return price_map.get(credit, 999999)

@router.post("/payment/create-checkout-session")
async def create_checkout_session(request: Request):
    """
    Stripe 결제 세션을 생성합니다.
    
    Args:
        request: FastAPI Request 객체
        
    Returns:
        Dict[str, Any]: 결제 세션 URL
        
    Raises:
        HTTPException: 결제 세션 생성 실패 시
    """
    try:
        data = await request.json()
        amount = data.get("credit_amount")
        
        if not amount or amount not in [500, 2000, 10000]:
            raise HTTPException(status_code=400, detail="Invalid credit amount")
            
        price = credit_to_price(amount)
        
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{amount} Intrix 크레딧",
                        "description": f"{amount} 크레딧을 구매합니다."
                    },
                    "unit_amount": price,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{os.getenv('FRONTEND_URL')}/mypage?success=true",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/purchase?canceled=true",
            metadata={
                "credit_amount": amount,
                "price": price
            }
        )
        
        logger.info(f"Checkout session created: {session.id}")
        return {"url": session.url}
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=500, detail="Payment processing error")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/payment/webhook")
async def stripe_webhook(request: Request):
    """
    Stripe 웹훅을 처리합니다.
    
    Args:
        request: FastAPI Request 객체
        
    Returns:
        Dict[str, str]: 처리 결과
        
    Raises:
        HTTPException: 웹훅 처리 실패 시
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except Exception as e:
        logger.error(f"Webhook signature verification failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    try:
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            email = session["customer_details"]["email"]
            credit_amount = int(session["metadata"]["credit_amount"])
            
            # TODO: 사용자 email 기반으로 크레딧 지급 처리
            # update_user_credit(email=email, amount=credit_amount)
            
            logger.info(f"Payment completed: {email} - {credit_amount} credits")
            
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing error") 