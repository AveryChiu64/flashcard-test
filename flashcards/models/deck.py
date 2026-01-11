from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Deck:
    """Represents a collection of flashcards."""
    id: Optional[int]
    name: str
    created_at: datetime
