from typing import List, Optional
from flashcards.models import Deck
from flashcards.storage.repositories import DeckRepository
from flashcards.services.validators import validate_deck

class DeckService:
    def __init__(self, deck_repo: DeckRepository):
        self.deck_repo = deck_repo

    def create_deck(self, name: str) -> Deck:
        validate_deck(name)
        return self.deck_repo.create(name)

    def get_all_decks(self) -> List[Deck]:
        return self.deck_repo.get_all()

    def delete_deck(self, deck_id: int):
        self.deck_repo.delete(deck_id)
