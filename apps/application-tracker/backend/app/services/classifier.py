from typing import Type, TypeVar
from pydantic import BaseModel
from openai import OpenAI

from app.schemas.updates import Updates

T = TypeVar("T", bound=BaseModel)


def run_structured_prompt(model_cls: Type[T], *, prompt: str, instructions: str) -> T:
    client = OpenAI()
    response = client.responses.parse(
        model="gpt-4o-mini",
        instructions=instructions,
        input=prompt,
        text_format=model_cls,
        max_output_tokens=500,
    )
    return response.output_parsed


def is_possibly_relevant(subject: str, body: str, sender: str, date) -> bool:
    instructions = """
Return true only if this email clearly refers to a specific job application the user has already submitted.

Return false for job suggestions, job alerts, recommendations, newsletters, generic job ads, networking, recruiter marketing, and career tips.

A suggested job is never an existing application.
If uncertain, return false.
"""

    class App_Relevant(BaseModel):
        is_relevant: bool

    response = run_structured_prompt(
        App_Relevant,
        prompt=f"Subject: {subject}, Body: {body}, Sender: {sender}, Date: {date}",
        instructions=instructions,
    )
    return response.is_relevant


def classify_email(subject: str, body: str, sender: str, date) -> Updates:
    instructions = "Extract the most relevant and recent information from this email regarding the job application."
    response = run_structured_prompt(
        Updates,
        prompt=f"Subject: {subject}\n\nBody: {body}\n\nSender: {sender}\n\nDate: {date}",
        instructions=instructions,
    )
    return response
