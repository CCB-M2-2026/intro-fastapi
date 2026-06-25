import pytest
from src.characters.application.delete_character import DeleteCharacter, DeleteCharacterCommand
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository
from src.characters.domain.value_objects import CharacterImg

class FakeCharacterRepository(CharacterRepository):
    def __init__(self):
        self._characters = {}
        self._next_id = 1
    
    def save(self, character: Character) -> None:
        self._characters[self._next_id] = character
        self._next_id += 1

    def all(self) -> list[Character]:
        return list(self._characters.values())
    
    def get_by_id(self, id: int) -> Character | None:
        return self._characters.get(id)
    
    def update(self, id: int, character: Character) -> Character | None:
        if id in self._characters:
            self._characters[id] = character
            return character
        return None
    
    def delete(self, id: int) -> bool:
        if id in self._characters:
            del self._characters[id]
            return True
        return False


class TestDeleteCharacter:
    def test_delete_character_success(self) -> None:
        character_repository = FakeCharacterRepository()
        
        character = Character(
            name="Tanjiro Kamado",
            state="alive",
            img=CharacterImg(value="https://example.com/tanjiro.jpg")
        )
        character_repository.save(character)
        
        result = DeleteCharacter(character_repository).execute(
            DeleteCharacterCommand(id=1)
        )
        
        assert result is True
    
    def test_delete_character_not_found(self) -> None:
        character_repository = FakeCharacterRepository()
        
        result = DeleteCharacter(character_repository).execute(
            DeleteCharacterCommand(id=999)
        )
        
        assert result is False