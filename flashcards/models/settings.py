from dataclasses import dataclass, field
from typing import List

@dataclass
class ReviewSettings:
    """Settings for the Spaced Repetition System."""
    new_cards_per_day: int = 20
    review_limit_per_day: int = 200
    learning_steps: List[int] = field(default_factory=lambda: [1, 10])
    graduating_interval: int = 1
    easy_interval: int = 4
    lapse_interval: int = 1
    leech_threshold: int = 8
