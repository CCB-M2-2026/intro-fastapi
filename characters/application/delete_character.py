from dataclasses import dataclass
from src.characters.domain.repositories import CharacterRepository

@dataclass
class DeleteCharacterCommand:
    id: int

class DeleteCharacter:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository
    
    def execute(self, command: DeleteCharacterCommand) -> bool:
        return self._character_repository.delete(command.id)