def validate_card(front: str, back: str):
    """
    Validates card data.
    Raises ValueError if invalid.
    """
    if not front or not front.strip():
        raise ValueError("Card front text cannot be empty.")
    if not back or not back.strip():
        raise ValueError("Card back text cannot be empty.")
