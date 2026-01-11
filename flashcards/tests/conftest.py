import pytest
import tempfile
import os
from flashcards.storage import Database, DeckRepository, CardRepository, ReviewRepository
from flashcards.services import CardService, ReviewService, DeckService

@pytest.fixture
def db():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    database = Database(path)
    database.initialize()
    yield database
    if os.path.exists(path):
        os.unlink(path)

@pytest.fixture
def services(db):
    deck_repo = DeckRepository(db)
    card_repo = CardRepository(db)
    review_repo = ReviewRepository(db)
    return {
        "deck_repo": deck_repo,
        "card_repo": card_repo,
        "review_repo": review_repo,
        "deck_service": DeckService(deck_repo),
        "card_service": CardService(card_repo, review_repo),
        "review_service": ReviewService(review_repo, card_repo)
    }
