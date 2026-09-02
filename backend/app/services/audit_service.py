"""
ScamTrap AI — Investigator Audit Trail Service (§ Phase 12)

Provides audit logging for all investigator operations (ingestion, query, export,
authentication, role changes) to ensure reproducibility and accountability.
Raw PII is strictly excluded from audit records.
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class AuditRecord(BaseModel):
    """Structured audit log record for security investigations."""
    id: str = Field(...)
    actor: str = Field(..., description="Username or Service Account initiating action.")
    role: str = Field(default="analyst", description="RBAC role of actor ('analyst', 'admin').")
    action: str = Field(..., description="Action name (e.g. 'INGEST_INCIDENT', 'COPILOT_QUERY', 'EXPORT_STIX').")
    target_id: Optional[str] = Field(default=None, description="Target resource ID.")
    target_type: Optional[str] = Field(default=None, description="Resource type ('incident', 'campaign', 'export').")
    operation_details: Dict[str, Any] = Field(default_factory=dict, description="Metadata parameters.")
    status: str = Field(default="SUCCESS", description="'SUCCESS', 'DENIED', or 'FAILED'.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditService:
    """In-memory & structured log audit recorder."""

    def __init__(self):
        self._audit_log: List[AuditRecord] = []

    def log_action(
        self,
        actor: str,
        action: str,
        role: str = "analyst",
        target_id: Optional[str] = None,
        target_type: Optional[str] = None,
        operation_details: Optional[Dict[str, Any]] = None,
        status: str = "SUCCESS",
    ) -> AuditRecord:
        import uuid
        record = AuditRecord(
            id=str(uuid.uuid4()),
            actor=actor,
            role=role,
            action=action,
            target_id=target_id,
            target_type=target_type,
            operation_details=operation_details or {},
            status=status,
        )
        self._audit_log.append(record)
        logger.info(
            "Audit event recorded",
            audit_id=record.id,
            actor=actor,
            role=role,
            action=action,
            target_id=target_id,
            status=status,
        )
        return record

    def get_audit_trail(self, limit: int = 50) -> List[AuditRecord]:
        return list(reversed(self._audit_log[-limit:]))


# Global singleton instance
audit_service = AuditService()
