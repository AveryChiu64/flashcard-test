from flashcards.models.settings import ReviewSettings

class SettingsService:
    def __init__(self):
        # In a real app, this might load from a DB or JSON file
        self._settings = ReviewSettings()

    def get_settings(self) -> ReviewSettings:
        return self._settings

    def update_settings(self, new_settings: ReviewSettings):
        self._settings = new_settings
