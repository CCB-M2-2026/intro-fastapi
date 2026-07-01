from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

class GetAllCharacters:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository
    
    def execute(self) -> list[Character]:
        return self._character_repository.all()