# email_schemas.py
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator


class EmailCategory(str, Enum):
    sales = "sales"
    marketing = "marketing"
    customer_support = "customer_support"
    technical = "technical"
    recruitment = "recruitment"
    legal = "legal"
    general = "general"


class EmailRequest(BaseModel):
    """
    User's high-level request.
    """
    user_input: str = Field(..., description="Raw user description / instruction")
    preferred_tone: Optional[str] = Field(
        None, description="e.g. 'formal', 'friendly', 'apologetic', 'persuasive'"
    )
    preferred_language: Optional[str] = Field(
        "en", description="Language code or descriptive language name"
    )


class EmailPlan(BaseModel):
    """
    Planning layer output.
    """
    category: EmailCategory
    tone: str
    language: str = "en"
    key_points: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    extra_fields_required: Dict[str, Any] = Field(default_factory=dict)


class EmailResponse(BaseModel):
    """
    Final generated email (structured output).
    """
    category: EmailCategory
    subject: str
    body: str
    tone: str
    language: str = "en"
    # Cross-category metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @validator("subject")
    def subject_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("subject must not be empty")
        return v.strip()

    @validator("body")
    def body_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("body must not be empty")
        return v.strip()
