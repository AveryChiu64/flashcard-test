from datetime import date

def test_review_correct(services):
    deck = services["deck_service"].create_deck("Deck 1")
    card = services["card_service"].add_card(deck.id, "Front", "Back")
    
    services["review_service"].record_review(card.id, is_correct=True)
    
    # Check that it's completed for today (not in due list)
    due = services["card_service"].get_due_cards()
    assert len(due) == 0
    
    # Check DB state: Due date should still be today (marked as "reviewed today")
    stored_card = services["card_repo"].get_by_deck(deck.id)[0]
    assert stored_card.due_date == date.today()
