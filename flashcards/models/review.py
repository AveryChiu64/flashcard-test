from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Review:
    """Represents a review event for a card."""
    id: Optional[int]
    card_id: int
    is_correct: bool
    reviewed_at: datetime
