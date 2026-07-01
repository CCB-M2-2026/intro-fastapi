import pytest
from src.characters.domain.exception import CharacterImgNotValid
from src.characters.application.create_character import CreateCharacter, CreateCharacterCommand
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


class TestCreateCharacter:
    # Happy path
    def test_create_character(self) -> None:
        character_repository = FakeCharacterRepository()

        """ esto nos permite inyectar la dependencia del repositorio falso en la clase CreateCharacter """
        CreateCharacter(character_repository).execute(
            CreateCharacterCommand(
                name="Tanjiro Kamado",
                state="alive",
                img="https://example.com/tanjiro.jpg"
            )
        )
        characters = character_repository.all()
        assert len(characters) == 1
        assert characters[0].name() == "Tanjiro Kamado"
        assert characters[0].state() == "alive"
        assert characters[0].img().value == "https://example.com/tanjiro.jpg"

    def test_create_character_fails_with_invalid_img(self) -> None:
        character_repository = FakeCharacterRepository()

        """ esto nos permite inyectar la dependencia del repositorio falso en la clase CreateCharacter """
        with pytest.raises(CharacterImgNotValid):
            CreateCharacter(character_repository).execute(
                CreateCharacterCommand(
                    name="Tanjiro Kamado",
                    state="alive",
                    img="invalid_img"
                )
            )
            
        characters = character_repository.all()
        assert len(characters) == 0