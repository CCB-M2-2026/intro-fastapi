import pytest
from src.characters.application.get_all_character import GetAllCharacters
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository
from src.characters.domain.value_objects import CharacterImg

class FakeCharacterRepository(CharacterRepository):
    def __init__(self):
        self._characters = []
    
    def save(self, character: Character) -> None:
        self._characters.append(character)

    def all(self) -> list[Character]:
        return list(self._characters)
    
    def get_by_id(self, id: int) -> Character | None:
        return None
    
    def update(self, id: int, character: Character) -> Character | None:
        return None
    
    def delete(self, id: int) -> bool:
        return True


class TestGetAllCharacters:
    def test_get_all_returns_all_characters(self) -> None:
        character_repository = FakeCharacterRepository()
        
        character1 = Character(
            name="Tanjiro Kamado",
            state="alive",
            img=CharacterImg(value="https://example.com/tanjiro.jpg")
        )
        character2 = Character(
            name="Nezuko Kamado",
            state="alive",
            img=CharacterImg(value="https://example.com/nezuko.jpg")
        )
        character_repository.save(character1)
        character_repository.save(character2)
        
        result = GetAllCharacters(character_repository).execute()
        
        assert len(result) == 2
        assert result[0].name() == "Tanjiro Kamado"
        assert result[1].name() == "Nezuko Kamado"
    
    def test_get_all_returns_empty_list(self) -> None:
        character_repository = FakeCharacterRepository()
        
        result = GetAllCharacters(character_repository).execute()
        
        assert len(result) == 0