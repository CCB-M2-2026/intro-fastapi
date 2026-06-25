from dataclasses import dataclass
from src.characters.domain.models import Character
from src.characters.domain.repository import CharacterRepository
from src.characters.domain.valid_object import CharacterImg

@dataclass
class CreateCharacterCommand:
    name: str
    state: str
    img: str

class CreateCharacter:
    def __init__(self, character_repository:CharacterRepository):
        self._character_repository = character_repository
    
    def execute(self,command:CreateCharacterCommand)->Character:
        character= Character(
            name=command.name,
            state=command.state,
            img=CharacterImg(value=command.img)
        )
        self._character_repository.save(character)
        return character
    
    