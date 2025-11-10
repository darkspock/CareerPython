"""Candidate Review Router."""
import logging
from typing import List, Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer

from adapters.http.company_app.candidate_review.schemas.create_review_request import CreateReviewRequest
from adapters.http.company_app.candidate_review.schemas.review_response import ReviewResponse
from adapters.http.company_app.candidate_review.schemas.update_review_request import UpdateReviewRequest
from core.container import Container
from src.framework.infrastructure.helpers.mixed_helper import MixedHelper
from adapters.http.company_app.company.controllers.review_controller import ReviewController

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/company/candidates", tags=["Candidate Reviews"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/companies/auth/login")


def get_company_user_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract company user ID from JWT token"""
    try:
        import base64
        import json
        
        # Decode JWT token (simple implementation, should use proper JWT library)
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        decoded = base64.urlsafe_b64decode(payload)
        data: dict[str, Any] = json.loads(decoded)
        
        company_user_id = data.get('company_user_id')
        if not company_user_id:
            raise HTTPException(status_code=401, detail="Token missing company_user_id")
        
        # Use MixedHelper to safely convert to string
        return MixedHelper.get_string(company_user_id)
    except Exception as e:
        log.error(f"Error extracting company_user_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/{company_candidate_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_review(
    company_candidate_id: str,
    request: CreateReviewRequest,
    controller: ReviewController = Depends(Provide[Container.review_controller]),
    company_user_id: str = Depends(get_company_user_id_from_token)
) -> ReviewResponse:
    """Create a new review for a candidate"""
    try:
        return controller.create_review(company_candidate_id, request, company_user_id)
    except ValueError as e:
        log.error(f"Validation error creating review: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error creating review: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{company_candidate_id}/reviews", response_model=List[ReviewResponse])
@inject
def list_reviews(
    company_candidate_id: str,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> List[ReviewResponse]:
    """Get all reviews for a candidate"""
    try:
        return controller.list_reviews_by_company_candidate(company_candidate_id)
    except Exception as e:
        log.error(f"Error listing reviews: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{company_candidate_id}/reviews/stage/{stage_id}", response_model=List[ReviewResponse])
@inject
def list_reviews_by_stage(
    company_candidate_id: str,
    stage_id: str,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> List[ReviewResponse]:
    """Get all reviews for a candidate in a specific stage"""
    try:
        return controller.list_reviews_by_stage(company_candidate_id, stage_id)
    except Exception as e:
        log.error(f"Error listing reviews by stage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{company_candidate_id}/reviews/global", response_model=List[ReviewResponse])
@inject
def list_global_reviews(
    company_candidate_id: str,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> List[ReviewResponse]:
    """Get all global reviews for a candidate"""
    try:
        return controller.list_global_reviews(company_candidate_id)
    except Exception as e:
        log.error(f"Error listing global reviews: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/reviews/{review_id}", response_model=ReviewResponse)
@inject
def get_review(
    review_id: str,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> ReviewResponse:
    """Get a review by ID"""
    result = controller.get_review_by_id(review_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return result


@router.put("/reviews/{review_id}", response_model=ReviewResponse)
@inject
def update_review(
    review_id: str,
    request: UpdateReviewRequest,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> ReviewResponse:
    """Update a review"""
    try:
        return controller.update_review(review_id, request)
    except ValueError as e:
        log.error(f"Validation error updating review: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error updating review: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_review(
    review_id: str,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> None:
    """Delete a review"""
    try:
        controller.delete_review(review_id)
    except Exception as e:
        log.error(f"Error deleting review: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/reviews/{review_id}/mark-reviewed", response_model=ReviewResponse)
@inject
def mark_review_as_reviewed(
    review_id: str,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> ReviewResponse:
    """Mark a review as reviewed"""
    try:
        return controller.mark_as_reviewed(review_id)
    except Exception as e:
        log.error(f"Error marking review as reviewed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/reviews/{review_id}/mark-pending", response_model=ReviewResponse)
@inject
def mark_review_as_pending(
    review_id: str,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> ReviewResponse:
    """Mark a review as pending"""
    try:
        return controller.mark_as_pending(review_id)
    except Exception as e:
        log.error(f"Error marking review as pending: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

