from pydantic import BaseModel
from datetime import datetime

from app.schemas.updates import Updates
from app.services.classifier import is_possibly_relevant, classify_email


class E_Mail(BaseModel):
    subject: str
    body: str
    sender: str
    date: datetime

    def is_possibly_relevant(self) -> bool:
        return is_possibly_relevant(self.subject, self.body, self.sender, self.date)

    def classify(self) -> Updates:
        return classify_email(self.subject, self.body, self.sender, self.date)
