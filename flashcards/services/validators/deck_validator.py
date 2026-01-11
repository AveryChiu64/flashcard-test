def validate_deck(name: str):
    """
    Validates deck data.
    Raises ValueError if invalid.
    """
    if not name or not name.strip():
        raise ValueError("Deck name cannot be empty.")
