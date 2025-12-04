# main.py
import asyncio
from email_schemas import EmailRequest
from pipeline import generate_email


async def demo():
    req = EmailRequest(
        user_input=(
            "A customer is unable to log into their account after resetting "
            "the password. Write a polite support email apologizing, "
            "explaining that we're investigating, and offering a manual reset link."
        ),
        preferred_tone="reassuring",
        preferred_language="en",
    )

    email, in_warnings, out_warnings = await generate_email(req)

    print("=== INPUT WARNINGS ===")
    for w in in_warnings:
        print("-", w)

    print("\n=== EMAIL GENERATED ===")
    print("Category:", email.category)
    print("Subject:", email.subject)
    print("\nBody:\n", email.body)

    print("\n=== OUTPUT WARNINGS ===")
    for w in out_warnings:
        print("-", w)


if __name__ == "__main__":
    asyncio.run(demo())
