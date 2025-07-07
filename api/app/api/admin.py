from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.schemas import (
    UserResponse, UserUpdate, AdminDashboardResponse, UserStatsResponse,
    DocumentStatsResponse, SystemStatsResponse, SystemMetricResponse, 
    SystemMetricCreate, VectorCollectionResponse, VectorCollectionCreate
)
from app.services import crud
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models import User, UserRole

router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)

def require_admin(current_user: User = Depends(get_current_active_user)):
    """Dependency to require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/dashboard", response_model=AdminDashboardResponse)
async def get_admin_dashboard(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard data with statistics and metrics"""
    try:
        user_stats = await crud.get_user_stats(db)
        document_stats = await crud.get_document_stats(db)
        recent_activities = await crud.get_recent_activities(db)
        
        # Mock system stats - in production, these would come from monitoring
        system_stats = {
            "api_calls_today": 1250,
            "average_response_time": 0.45,
            "system_uptime": "99.8%",
            "active_sessions": 23
        }
        
        return AdminDashboardResponse(
            user_stats=UserStatsResponse(**user_stats),
            document_stats=DocumentStatsResponse(**document_stats),
            system_stats=SystemStatsResponse(**system_stats),
            recent_activities=recent_activities
        )
    except Exception as e:
        logger.error(f"Error fetching admin dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard data")

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    try:
        users = await crud.get_all_users(db, skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update user information (admin only)"""
    try:
        updated_user = await crud.update_user(db, user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(updated_user)
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")

@router.get("/metrics")
async def get_system_metrics(
    metric_name: str = None,
    days: int = 7,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get system metrics (admin only)"""
    try:
        # For now, return empty list as metrics need to be implemented
        return []
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch metrics")

@router.post("/metrics")
async def create_system_metric(
    metric: SystemMetricCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new system metric (admin only)"""
    try:
        # For now, return a simple response as metrics need to be implemented
        return {"message": "Metric creation to be implemented", "metric_name": metric.metric_name}
    except Exception as e:
        logger.error(f"Error creating metric: {e}")
        raise HTTPException(status_code=500, detail="Failed to create metric")

@router.get("/vector-collections")
async def get_vector_collections(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all vector collections (admin only)"""
    try:
        # For now, return empty list as vector collections need to be implemented
        return []
    except Exception as e:
        logger.error(f"Error fetching vector collections: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch vector collections")

@router.post("/vector-collections")
async def create_vector_collection(
    collection: VectorCollectionCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new vector collection (admin only)"""
    try:
        # For now, return a simple response as vector collections need to be implemented
        return {"message": "Vector collection creation to be implemented", "collection_name": collection.collection_name}
    except Exception as e:
        logger.error(f"Error creating vector collection: {e}")
        raise HTTPException(status_code=500, detail="Failed to create vector collection")

@router.post("/vector-upload")
async def upload_to_vector_store(
    collection_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Upload documents to vector store (admin only)"""
    try:
        # This would integrate with the vector store to upload documents
        # For now, just return a success message
        return {"message": "Vector upload functionality to be implemented"}
    except Exception as e:
        logger.error(f"Error uploading to vector store: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload to vector store")
