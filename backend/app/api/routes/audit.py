from fastapi import APIRouter
from app.audit.audit_chain import audit_logger

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/verify")
async def verify_audit_integrity():
    is_valid, details = audit_logger.verify_integrity()

    return {
        "integrity": "valid" if is_valid else "tampered",
        "valid": is_valid,
        "error": details,
        "total_entries": audit_logger._get_count()
    }


@router.get("/logs")
async def get_audit_logs():
    return audit_logger.get_all_entries()


@router.get("/logs/{user_id}")
async def get_user_audit_logs(user_id: str):
    return audit_logger.get_entries_by_user(user_id)