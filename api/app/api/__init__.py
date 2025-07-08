from .documents import router as documents_router
from .chat import router as chat_router
from .query import router as query_router
from .admin import router as admin_router
from .legal import router as legal_router

__all__ = ["documents_router", "chat_router", "query_router", "admin_router", "legal_router"]
