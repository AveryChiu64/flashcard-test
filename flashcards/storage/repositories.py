from datetime import datetime, date
from typing import List, Optional
from flashcards.models import Deck, Card, Review
from flashcards.storage.database import Database

class DeckRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, name: str) -> Deck:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now()
            cursor.execute(
                "INSERT INTO decks (name, created_at) VALUES (?, ?)",
                (name, now)
            )
            conn.commit()
            return Deck(id=cursor.lastrowid, name=name, created_at=now)

    def get_all(self) -> List[Deck]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM decks").fetchall()
            return [
                Deck(
                    id=row["id"],
                    name=row["name"],
                    created_at=datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"]
                )
                for row in rows
            ]

    def delete(self, deck_id: int):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
            conn.commit()

class CardRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, deck_id: int, front: str, back: str, due_date: Optional[date] = None) -> Card:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now()
            due = due_date if due_date else date.today()
            cursor.execute(
                """
                INSERT INTO cards (deck_id, front_text, back_text, due_date, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (deck_id, front, back, due, now)
            )
            conn.commit()
            return Card(
                id=cursor.lastrowid,
                deck_id=deck_id,
                front_text=front,
                back_text=back,
                due_date=due,
                created_at=now
            )

    def get_by_deck(self, deck_id: int) -> List[Card]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM cards WHERE deck_id = ?", (deck_id,)).fetchall()
            return [
                Card(
                    id=row["id"],
                    deck_id=row["deck_id"],
                    front_text=row["front_text"],
                    back_text=row["back_text"],
                    due_date=date.fromisoformat(row["due_date"]) if isinstance(row["due_date"], str) else row["due_date"],
                    created_at=datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"]
                )
                for row in rows
            ]

    def get_due_cards(self, target_date: date = None) -> List[Card]:
        target = target_date if target_date else date.today()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM cards WHERE due_date <= ?", (target,)).fetchall()
            return [
                Card(
                    id=row["id"],
                    deck_id=row["deck_id"],
                    front_text=row["front_text"],
                    back_text=row["back_text"],
                    due_date=date.fromisoformat(row["due_date"]) if isinstance(row["due_date"], str) else row["due_date"],
                    created_at=datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"]
                )
                for row in rows
            ]
    
    def update_due_date(self, card_id: int, new_due_date: date):
        with self.db.get_connection() as conn:
            conn.execute("UPDATE cards SET due_date = ? WHERE id = ?", (new_due_date, card_id))
            conn.commit()

class ReviewRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, card_id: int, is_correct: bool) -> Review:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now()
            cursor.execute(
                "INSERT INTO reviews (card_id, is_correct, reviewed_at) VALUES (?, ?, ?)",
                (card_id, is_correct, now)
            )
            conn.commit()
            return Review(
                id=cursor.lastrowid,
                card_id=card_id,
                is_correct=is_correct,
                reviewed_at=now
            )

    def get_card_ids_reviewed_on_date(self, date_query: date) -> set[int]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            # SQLite date() returns YYYY-MM-DD from timestamp string
            rows = cursor.execute(
                "SELECT card_id FROM reviews WHERE date(reviewed_at) = ?",
                (date_query.isoformat(),)
            ).fetchall()
            return {row["card_id"] for row in rows}
