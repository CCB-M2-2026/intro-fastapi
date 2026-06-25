from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

class GetCharacterById:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository
    
    def execute(self, id: int) -> Character | None:
        return self._character_repository.get_by_id(id)