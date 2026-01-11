import sys
from datetime import date
from typing import Optional

from flashcards.storage import Database, DeckRepository, CardRepository, ReviewRepository
from flashcards.services import CardService, ReviewService, DeckService, Clock
from flashcards.models import Deck, Card

class FlashcardCLI:
    def __init__(self):
        # Initialize dependencies
        self.db = Database("flashcards.db")
        self.db.initialize()
        
        self.deck_repo = DeckRepository(self.db)
        self.card_repo = CardRepository(self.db)
        self.review_repo = ReviewRepository(self.db)
        
        self.clock = Clock()
        self.card_service = CardService(self.card_repo, self.review_repo, self.clock)
        self.review_service = ReviewService(self.review_repo, self.card_repo, self.clock)
        self.deck_service = DeckService(self.deck_repo)

    def run(self):
        while True:
            print("\n--- Flashcard App ---")
            print("1. Study")
            print("2. Manage Decks")
            print("3. Quit")
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.study_mode()
            elif choice == "2":
                self.manage_decks()
            elif choice == "3":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid option.")

    def manage_decks(self):
        while True:
            print("\n--- Manage Decks ---")
            print("1. List Decks")
            print("2. Create Deck")
            print("3. Delete Deck")
            print("4. Add Card to Deck")
            print("5. Back")
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.list_decks()
            elif choice == "2":
                self.create_deck()
            elif choice == "3":
                self.delete_deck()
            elif choice == "4":
                self.add_card()
            elif choice == "5":
                break
            else:
                print("Invalid option.")

    def list_decks(self):
        decks = self.deck_service.get_all_decks()
        if not decks:
            print("No decks found.")
        else:
            print("\nDecks:")
            for deck in decks:
                print(f"- [{deck.id}] {deck.name}")

    def create_deck(self):
        name = input("Enter deck name: ").strip()
        if name:
            deck = self.deck_service.create_deck(name)
            print(f"Deck '{deck.name}' created.")

    def delete_deck(self):
        self.list_decks()
        try:
            deck_id = int(input("Enter Deck ID to delete: "))
            self.deck_service.delete_deck(deck_id)
            print("Deck deleted.")
        except ValueError:
            print("Invalid ID.")

    def add_card(self):
        self.list_decks()
        try:
            deck_id = int(input("Enter target Deck ID: "))
            front = input("Front Text: ").strip()
            back = input("Back Text: ").strip()
            if front and back:
                self.card_service.add_card(deck_id, front, back)
                print("Card added.")
            else:
                print("Front and Back text are required.")
        except ValueError:
            print("Invalid ID.")

    def study_mode(self):
        due_cards = self.card_service.get_due_cards()
        if not due_cards:
            print("No cards due today!")
            return

        print(f"\nStudying {len(due_cards)} due cards...")
        for card in due_cards:
            print(f"\nFront: {card.front_text}")
            input("Press Enter to show back...")
            print(f"Back: {card.back_text}")
            
            while True:
                result = input("Did you get it right? (y/n): ").lower().strip()
                if result == 'y':
                    self.review_service.record_review(card.id, True)
                    print("Marked correct.")
                    break
                elif result == 'n':
                    self.review_service.record_review(card.id, False)
                    print("Marked incorrect (due tomorrow).")
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    app = FlashcardCLI()
    app.run()
