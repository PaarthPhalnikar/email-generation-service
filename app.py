# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from email_schemas import EmailRequest, EmailResponse
from pipeline import generate_email

app = FastAPI(title="Email Generation Service")


class GenerateEmailRequest(BaseModel):
    user_input: str
    preferred_tone: Optional[str] = None
    preferred_language: Optional[str] = "en"


class GenerateEmailResponse(BaseModel):
    email: EmailResponse
    input_warnings: List[str]
    output_warnings: List[str]


@app.get("/")
async def root():
    """Simple health check endpoint for Render."""
    return {"status": "ok", "service": "email-generator"}


@app.post("/generate-email", response_model=GenerateEmailResponse)
async def generate_email_endpoint(body: GenerateEmailRequest):
    req = EmailRequest(
        user_input=body.user_input,
        preferred_tone=body.preferred_tone,
        preferred_language=body.preferred_language,
    )

    try:
        email, in_warnings, out_warnings = await generate_email(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return GenerateEmailResponse(
        email=email,
        input_warnings=in_warnings,
        output_warnings=out_warnings,
    )
