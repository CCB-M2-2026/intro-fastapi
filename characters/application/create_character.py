from dataclasses import dataclass
from src.characters.domain.value_objects import CharacterImg
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

@dataclass
class CreateCharacterCommand:
    name: str
    state: str
    img: str

class CreateCharacter:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository

    def execute(self, command: CreateCharacterCommand) -> Character:
        character_img = CharacterImg(value=command.img)
        character = Character.create(
            name=command.name,
            state=command.state,
            img=character_img
        )
        return self._character_repository.save(character)