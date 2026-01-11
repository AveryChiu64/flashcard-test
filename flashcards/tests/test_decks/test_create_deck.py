def test_create_deck(services):
    deck = services["deck_service"].create_deck("New Deck")
    assert deck.id is not None
    assert deck.name == "New Deck"
