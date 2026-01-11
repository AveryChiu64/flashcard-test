from datetime import date, timedelta

def test_repeat_next_day(services):
    # This is similar to review_incorrect but explicitly named as requested
    deck = services["deck_service"].create_deck("Deck 1")
    card = services["card_service"].add_card(deck.id, "Front", "Back")
    
    services["review_service"].record_review(card.id, is_correct=False)
    
    updated_card = services["card_repo"].get_by_deck(deck.id)[0]
    tomorrow = date.today() + timedelta(days=1)
    
    assert updated_card.due_date == tomorrow
