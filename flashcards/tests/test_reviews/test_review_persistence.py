def test_review_persistence(services):
    deck = services["deck_service"].create_deck("Deck 1")
    card = services["card_service"].add_card(deck.id, "Front", "Back")
    
    services["review_service"].record_review(card.id, is_correct=True)
    
    # Check that a review record exists for this card
    # We need a method to get reviews for a card or just check raw DB
    # The current repo API doesn't expose get_reviews_by_card, so we check side effects 
    # or add a helper if needed. Alternatively, use get_card_ids_reviewed_on_date.
    
    from datetime import date
    reviewed_ids = services["review_repo"].get_card_ids_reviewed_on_date(date.today())
    assert card.id in reviewed_ids
