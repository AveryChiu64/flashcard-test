from datetime import date

def test_create_card(services):
    deck = services["deck_service"].create_deck("Deck 1")
    card = services["card_service"].add_card(deck.id, "Front", "Back")
    
    assert card.id is not None
    assert card.deck_id == deck.id
    assert card.front_text == "Front"
    assert card.due_date == date.today()
