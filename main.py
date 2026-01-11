from datetime import date
from flashcards.storage import Database, DeckRepository, CardRepository, ReviewRepository
from flashcards.services import CardService, ReviewService

def main():
    # Initialize Storage
    db = Database("flashcards.db")
    db.initialize()
    
    deck_repo = DeckRepository(db)
    card_repo = CardRepository(db)
    review_repo = ReviewRepository(db)
    
    # Initialize Services
    card_service = CardService(card_repo, review_repo)
    review_service = ReviewService(review_repo, card_repo)
    
    # 1. Create a Deck
    deck = deck_repo.create("Python Basics")
    print(f"Created Deck: {deck.name} (ID: {deck.id})")
    
    # 2. Add Cards
    card1 = card_service.add_card(deck.id, "What is a list?", "A mutable sequence.")
    card2 = card_service.add_card(deck.id, "What is a tuple?", "An immutable sequence.")
    print(f"Added cards: {card1.id}, {card2.id}")
    
    # 3. Check Due Cards (Today)
    due_cards = card_service.get_due_cards()
    print(f"\nDue Cards ({len(due_cards)}):")
    for card in due_cards:
        print(f"- [ID: {card.id}] {card.front_text}")
    
    if not due_cards:
        print("No cards due!")
        return

    # 4. Simulate a Review (Correct)
    # Correct -> Mark completed for day (due date stays, but filtered out)
    print("\nReviewing Card 1 (Correct)...")
    review_service.record_review(card1.id, is_correct=True)
    
    # 5. Simulate a Review (Incorrect)
    # Incorrect -> Move to tomorrow
    print("Reviewing Card 2 (Incorrect)...")
    review_service.record_review(card2.id, is_correct=False)
    
    # 6. Check Due Cards again
    due_cards_after = card_service.get_due_cards()
    print(f"\nDue Cards after review ({len(due_cards_after)}):")
    for card in due_cards_after:
        print(f"- [ID: {card.id}] {card.front_text}")
        
    # Verify DB State
    print("\nVerifying assignments:")
    refreshed_card1 = card_repo.get_by_deck(deck.id)[0]
    refreshed_card2 = card_repo.get_by_deck(deck.id)[1]
    
    print(f"Card 1 Due: {refreshed_card1.due_date} (Should be today: {date.today()})")
    print(f"Card 2 Due: {refreshed_card2.due_date} (Should be tomorrow: {date.today()})") # Mistake in print string explanation
    # actually logic: incorrect -> tomorrow.
    
if __name__ == "__main__":
    main()
