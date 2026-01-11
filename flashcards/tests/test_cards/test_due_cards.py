from datetime import date

def test_get_due_cards(services):
    deck = services["deck_service"].create_deck("Deck 1")
    card1 = services["card_service"].add_card(deck.id, "Due", "Back")
    
    due = services["card_service"].get_due_cards()
    assert len(due) == 1
    assert due[0].id == card1.id
