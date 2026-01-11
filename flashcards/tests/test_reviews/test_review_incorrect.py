from datetime import date, timedelta

def test_review_incorrect(services):
    deck = services["deck_service"].create_deck("Deck 1")
    card = services["card_service"].add_card(deck.id, "Front", "Back")
    
    services["review_service"].record_review(card.id, is_correct=False)
    
    # Check that it's moved to tomorrow
    stored_card = services["card_repo"].get_by_deck(deck.id)[0]
    expected_due = date.today() + timedelta(days=1)
    assert stored_card.due_date == expected_due
    
    # Check not due today
    due = services["card_service"].get_due_cards()
    assert len(due) == 0
