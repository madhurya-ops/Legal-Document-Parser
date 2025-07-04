from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
import logging

from .. import crud, schemas, auth
from ..database import get_db
from ..models import UserRole

router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)

def require_admin(current_user: schemas.UserResponse = Depends(auth.get_current_active_user)):
    """Dependency to require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/dashboard", response_model=schemas.AdminDashboardResponse)
async def get_admin_dashboard(
    current_user: schemas.UserResponse = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard data with statistics and metrics"""
    try:
        user_stats = crud.get_user_stats(db)
        document_stats = crud.get_document_stats(db)
        recent_activities = crud.get_recent_activities(db)
        
        # Mock system stats - in production, these would come from monitoring
        system_stats = {
            "api_calls_today": 1250,
            "average_response_time": 0.45,
            "system_uptime": "99.8%",
            "active_sessions": 23
        }
        
        return schemas.AdminDashboardResponse(
            user_stats=schemas.UserStatsResponse(**user_stats),
            document_stats=schemas.DocumentStatsResponse(**document_stats),
            system_stats=schemas.SystemStatsResponse(**system_stats),
            recent_activities=recent_activities
        )
    except Exception as e:
        logger.error(f"Error fetching admin dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard data")

@router.get("/users", response_model=List[schemas.UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.UserResponse = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    try:
        users = crud.get_all_users(db, skip=skip, limit=limit)
        return [schemas.UserResponse.from_orm(user) for user in users]
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: str,
    user_update: schemas.UserUpdate,
    current_user: schemas.UserResponse = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update user information (admin only)"""
    try:
        updated_user = crud.update_user(db, user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return schemas.UserResponse.from_orm(updated_user)
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")

@router.get("/metrics", response_model=List[schemas.SystemMetricResponse])
async def get_system_metrics(
    metric_name: str = None,
    days: int = 7,
    current_user: schemas.UserResponse = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get system metrics (admin only)"""
    try:
        if metric_name:
            metrics = crud.get_recent_metrics(db, metric_name, days)
        else:
            # Get all recent metrics - this would need to be implemented in crud
            metrics = []
        
        return [schemas.SystemMetricResponse.from_orm(metric) for metric in metrics]
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch metrics")

@router.post("/metrics", response_model=schemas.SystemMetricResponse)
async def create_system_metric(
    metric: schemas.SystemMetricCreate,
    current_user: schemas.UserResponse = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new system metric (admin only)"""
    try:
        db_metric = crud.create_system_metric(db, metric)
        return schemas.SystemMetricResponse.from_orm(db_metric)
    except Exception as e:
        logger.error(f"Error creating metric: {e}")
        raise HTTPException(status_code=500, detail="Failed to create metric")

@router.get("/vector-collections", response_model=List[schemas.VectorCollectionResponse])
async def get_vector_collections(
    current_user: schemas.UserResponse = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all vector collections (admin only)"""
    try:
        collections = crud.get_vector_collections(db)
        return [schemas.VectorCollectionResponse.from_orm(collection) for collection in collections]
    except Exception as e:
        logger.error(f"Error fetching vector collections: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch vector collections")

@router.post("/vector-collections", response_model=schemas.VectorCollectionResponse)
async def create_vector_collection(
    collection: schemas.VectorCollectionCreate,
    current_user: schemas.UserResponse = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new vector collection (admin only)"""
    try:
        db_collection = crud.create_vector_collection(db, collection, str(current_user.id))
        return schemas.VectorCollectionResponse.from_orm(db_collection)
    except Exception as e:
        logger.error(f"Error creating vector collection: {e}")
        raise HTTPException(status_code=500, detail="Failed to create vector collection")

@router.post("/vector-upload")
async def upload_to_vector_store(
    # files: List[UploadFile] = File(...),
    collection_id: str,
    current_user: schemas.UserResponse = Depends(require_admin),
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
