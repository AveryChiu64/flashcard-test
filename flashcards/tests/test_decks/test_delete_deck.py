def test_delete_deck(services):
    deck = services["deck_service"].create_deck("To Delete")
    services["deck_service"].delete_deck(deck.id)
    
    decks = services["deck_service"].get_all_decks()
    assert len(decks) == 0
