# pipeline.py
import json
from typing import Tuple, List
from openai import AsyncOpenAI
from pydantic import ValidationError

from config import openai_client, PLANNER_MODEL, GENERATOR_MODEL
from email_schemas import EmailRequest, EmailPlan, EmailResponse
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
        # Force JSON output from the model
        response_format={"type": "json_object"},
    )

    content = resp.choices[0].message.content

    if not content or not content.strip():
        # This will show up in the /generate-email error message
        raise RuntimeError("Planner returned empty content – check model name and API key.")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        # Help debug by showing first part of the response
        preview = content[:200].replace("\n", " ")
        raise Runtim
