# config.py
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  # optional

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in .env")

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Models – you can tweak these
PLANNER_MODEL = "gpt-4o-mini"
GENERATOR_MODEL = "gpt-4o"
