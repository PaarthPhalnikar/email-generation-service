# pipeline.py
import json
from typing import Tuple, List
from openai import AsyncOpenAI
from pydantic import ValidationError

from config import openai_client, PLANNER_MODEL, GENERATOR_MODEL
from email_schemas import EmailRequest, EmailPlan, EmailResponse, EmailCategory
from guardrails import check_input_guardrails, check_output_guardrails, GuardrailError
from prompts import PLANNER_SYSTEM_PROMPT, GENERATOR_SYSTEM_PROMPT


async def run_planner(
    client: AsyncOpenAI,
    req: EmailRequest,
) -> EmailPlan:
    messages = [
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"USER_INPUT:\n{req.user_input}\n\n"
                f"PREFERRED_TONE: {req.preferred_tone or 'unspecified'}\n"
                f"PREFERRED_LANGUAGE: {req.preferred_language or 'en'}"
            ),
        },
    ]

    resp = await client.chat.completions.create(
        model=PLANNER_MODEL,
        messages=messages,
        temperature=0.3,
    )

    content = resp.choices[0].message.content
    data = json.loads(content)  # will raise if not valid JSON

    # Fallback: if model didn't respect language, override with user preference
    if req.preferred_language:
        data["language"] = req.preferred_language

    plan = EmailPlan.model_validate(data)
    return plan


async def run_generator(
    client: AsyncOpenAI,
    req: EmailRequest,
    plan: EmailPlan,
) -> EmailResponse:
    user_prompt = {
        "role": "user",
        "content": json.dumps(
            {
                "user_input": req.user_input,
                "plan": plan.model_dump(),
            },
            ensure_ascii=False,
        ),
    }

    resp = await client.chat.completions.create(
        model=GENERATOR_MODEL,
        messages=[
            {"role": "system", "content": GENERATOR_SYSTEM_PROMPT},
            user_prompt,
        ],
        temperature=0.7,
    )

    content = resp.choices[0].message.content
    data = json.loads(content)
    email = EmailResponse.model_validate(data)
    return email


async def generate_email(req: EmailRequest) -> Tuple[EmailResponse, List[str], List[str]]:
    """
    Full pipeline:
    - Input guardrails
    - Planner model
    - Generator model
    - Output guardrails

    Returns: (email, input_warnings, output_warnings)
    """
    # 1. Input guardrails
    input_warnings = check_input_guardrails(req)

    # 2. Planning layer
    plan = await run_planner(openai_client, req)

    # 3. Generation layer
    email = await run_generator(openai_client, req, plan)

    # 4. Output guardrails
    output_warnings = check_output_guardrails(email)

    return email, input_warnings, output_warnings
