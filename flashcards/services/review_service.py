from datetime import date, timedelta
from flashcards.models import Review
from flashcards.storage.repositories import ReviewRepository, CardRepository
from flashcards.services.clock import Clock

class ReviewService:
    def __init__(self, review_repo: ReviewRepository, card_repo: CardRepository, clock: Clock):
        self.review_repo = review_repo
        self.card_repo = card_repo
        self.clock = clock

    def record_review(self, card_id: int, is_correct: bool) -> Review:
        """
        Records a review and updates the card's due date.
        
        Rule:
        - Correct -> Keep due_date as-is (completed for today logic handled in CardService)
        - Incorrect -> Set due_date to tomorrow
        """
        # 1. Record the review
        review = self.review_repo.create(card_id, is_correct)
        
        # 2. Update card due date if incorrect
        if not is_correct:
            tomorrow = self.clock.today() + timedelta(days=1)
            self.card_repo.update_due_date(card_id, tomorrow)
        
        # If correct, due_date stays as-is (per requirements)
        
        return review
