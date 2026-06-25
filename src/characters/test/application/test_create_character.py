import pytest
from src.characters.application.create_character import CreateCharacter,CreateCharacterCommand
from src.characters.domain.models import Character
from src.characters.domain.repository import CharacterRepository

class FakeCharacterRepository(CharacterRepository):
    def __init__(self):
            self._characters = []
    def save(self,character: Character)->None:
        self._characters.append(character)
    def all(self)->list[Character]:
        return list(self._characters)
    
class TestCreateCharacter:
    def test_create_character(self) ->None:
        character_repository = FakeCharacterRepository()
        
        CreateCharacter(character_repository).execute(
            CreateCharacterCommand(
                name="Tanjiro Kamado",
                state="alive",
                img="https://example.com/tanjiro.jpg"
            )
        )
        characters= character_repository.all()
        assert len(characters) == 1
    
    def test_create_character_fails_with_invalid_url(self)->None:
        character_repository = FakeCharacterRepository()
        
        with pytest.raises(Exception):
            CreateCharacter(character_repository).execute(
                CreateCharacterCommand(
                    name="Tanjiro Kamado",
                    state="alive",
                    img="invalid_img"
                )
            )
        characters= character_repository.all()
        assert len(characters) == 0