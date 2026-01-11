from datetime import date
from typing import List
from flashcards.models import Card
from flashcards.storage.repositories import CardRepository, ReviewRepository
from flashcards.services.clock import Clock

class CardService:
    def __init__(self, card_repo: CardRepository, review_repo: ReviewRepository, clock: Clock):
        self.card_repo = card_repo
        self.review_repo = review_repo
        self.clock = clock

    def add_card(self, deck_id: int, front: str, back: str) -> Card:
        """Adds a new card to a deck."""
        # We pass explicit today from clock to ensure consistency
        return self.card_repo.create(deck_id, front, back, due_date=self.clock.today())

    def get_due_cards(self, target_date: date = None) -> List[Card]:
        """
        Returns cards that are due on or before the target date.
        
        Logic:
        1. Card due_date <= target_date
        2. Card has NOT been reviewed on target_date (if target_date is today/specific day)
           Note: The requirement is 'correct -> mark completed for day'.
           Since 'correct' keeps due_date as-is (e.g. today), we must filter out
           cards reviewed successfully OR unsuccessfully today to avoid repetition?
           Prompt: 'If a user answers a card incorrectly, schedule it to be reviewed again the next day.'
           This means incorrect cards change due date to tomorrow, so they won't appear in 'due <= today' check.
           Prompt: 'If a user answers a card correctly, mark it as completed for the day. ... correct -> keep due_date as-is'.
           This means correct cards stay due=today, BUT shouldn't be shown again.
           So we explicitly filter out any card reviewed on 'target_date'.
        """
        today = target_date if target_date else self.clock.today()
        
        # Get all potential candidates
        candidates = self.card_repo.get_due_cards(today)
        
        # Get IDs of cards already reviewed today
        reviewed_ids = self.review_repo.get_card_ids_reviewed_on_date(today)
        
        # Filter
        return [c for c in candidates if c.id not in reviewed_ids]
