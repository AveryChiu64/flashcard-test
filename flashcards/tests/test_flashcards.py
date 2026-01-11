import pytest
from datetime import date, timedelta
from flashcards.storage import Database, DeckRepository, CardRepository, ReviewRepository
from flashcards.services import CardService, ReviewService

import tempfile
import os

@pytest.fixture
def db():
    # Use a temporary file for DB tests to ensure persistence across connections
    # while keeping isolation.
    fd, path = tempfile.mkstemp()
    os.close(fd) # Close file descriptor, let sqlite open it
    
    database = Database(path)
    database.initialize()
    
    yield database
    
    # Cleanup
    if os.path.exists(path):
        os.unlink(path)

@pytest.fixture
def services(db):
    deck_repo = DeckRepository(db)
    card_repo = CardRepository(db)
    review_repo = ReviewRepository(db)
    return {
        "deck": deck_repo,
        "card": card_repo,
        "review": review_repo,
        "card_service": CardService(card_repo, review_repo),
        "review_service": ReviewService(review_repo, card_repo)
    }

def test_create_deck(services):
    deck = services["deck"].create("Test Deck")
    assert deck.id is not None
    assert deck.name == "Test Deck"

def test_add_card(services):
    deck = services["deck"].create("Test Deck")
    card = services["card_service"].add_card(deck.id, "Front", "Back")
    assert card.id is not None
    assert card.deck_id == deck.id
    assert card.due_date == date.today()

def test_review_correct_behavior(services):
    """
    If correct:
    - Due date remains today
    - Card is marked completed for the day (not in due list)
    """
    deck = services["deck"].create("Test Deck")
    card = services["card_service"].add_card(deck.id, "Front", "Back")
    
    # Initially due
    due = services["card_service"].get_due_cards()
    assert len(due) == 1
    assert due[0].id == card.id
    
    # Review Correct
    services["review_service"].record_review(card.id, is_correct=True)
    
    # Check DB state
    updated_card = services["card"].get_by_deck(deck.id)[0]
    assert updated_card.due_date == date.today()
    
    # Check Service logic (should filter out)
    due_after = services["card_service"].get_due_cards()
    assert len(due_after) == 0

def test_review_incorrect_behavior(services):
    """
    If incorrect:
    - Due date moves to tomorrow
    """
    deck = services["deck"].create("Test Deck")
    card = services["card_service"].add_card(deck.id, "Front", "Back")
    
    # Review Incorrect
    services["review_service"].record_review(card.id, is_correct=False)
    
    # Check DB state
    updated_card = services["card"].get_by_deck(deck.id)[0]
    expected_tomorrow = date.today() + timedelta(days=1)
    assert updated_card.due_date == expected_tomorrow
    
    # Check Service logic (should not be due today)
    due_after = services["card_service"].get_due_cards()
    assert len(due_after) == 0
