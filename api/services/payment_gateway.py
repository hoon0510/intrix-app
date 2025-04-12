"""
Payment Gateway Service for handling Stripe payments and credit management
"""

import os
from typing import Dict, List
from fastapi import APIRouter, HTTPException, Request
from dotenv import load_dotenv
import stripe
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe_webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

# Initialize router
router = APIRouter(prefix="/payment", tags=["payment"])

# Mock database for transactions (replace with actual database)
transactions = []

async def create_checkout_session(price_id: str, user_id: str) -> Dict:
    """
    Create a Stripe Checkout session for credit purchase
    
    Args:
        price_id: Stripe price ID for the credit package
        user_id: User ID of the purchaser
        
    Returns:
        Dict containing the checkout session URL
    """
    try:
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{os.getenv('FRONTEND_URL')}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/payment/cancel",
            metadata={
                'user_id': user_id
            }
        )
        
        return {
            'session_id': session.id,
            'url': session.url
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def webhook_handler(request: Request) -> Dict:
    """
    Handle Stripe webhook events
    
    Args:
        request: FastAPI request object containing the webhook payload
        
    Returns:
        Dict containing the status of the webhook processing
    """
    try:
        # Get the webhook payload
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
        
        # Handle the event
        if event.type == 'checkout.session.completed':
            session = event.data.object
            
            # Get the user ID from the session metadata
            user_id = session.metadata.get('user_id')
            if not user_id:
                raise HTTPException(status_code=400, detail="User ID not found in session metadata")
            
            # Get the amount paid (in cents)
            amount = session.amount_total / 100
            
            # Calculate credits (1 credit = $1)
            credits = int(amount)
            
            # Record the transaction
            transaction = {
                'user_id': user_id,
                'amount': amount,
                'credits': credits,
                'timestamp': datetime.now().isoformat(),
                'status': 'completed',
                'session_id': session.id
            }
            transactions.append(transaction)
            
            # TODO: Add credits to user's balance in the database
            # await credit_manager.add_credits(user_id, credits)
            
            return {'status': 'success', 'message': 'Payment processed successfully'}
            
        return {'status': 'success', 'message': 'Event processed'}
        
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_transaction_history(user_id: str) -> List[Dict]:
    """
    Get transaction history for a user
    
    Args:
        user_id: User ID to get transactions for
        
    Returns:
        List of transaction records
    """
    try:
        # Filter transactions for the user
        user_transactions = [
            t for t in transactions if t['user_id'] == user_id
        ]
        
        return user_transactions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoints
@router.post("/create-checkout-session")
async def create_checkout_session_endpoint(price_id: str, user_id: str):
    return await create_checkout_session(price_id, user_id)

@router.post("/webhook")
async def webhook_endpoint(request: Request):
    return await webhook_handler(request)

@router.get("/transactions/{user_id}")
async def get_transaction_history_endpoint(user_id: str):
    return await get_transaction_history(user_id) 