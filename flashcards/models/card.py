from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Card:
    """Represents a single flashcard."""
    id: Optional[int]
    deck_id: int
    front_text: str
    back_text: str
    due_date: date
    created_at: datetime
