from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    # v1 schema implementation
    document_id: str
    content: str
    source_type: str  # e.g., 'PDF', 'Video', 'HTML', 'CSV', 'Code', 'Transcript'
    author: Optional[str] = "Unknown"
    timestamp: Optional[datetime] = None

    # Generic container for source-specific metadata
    source_metadata: dict = Field(default_factory=dict)

    class Config:
        orm_mode = True
