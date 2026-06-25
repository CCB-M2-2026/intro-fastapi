import pytest
from src.characters.application.update_character import UpdateCharacter, UpdateCharacterCommand
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository
from src.characters.domain.value_objects import CharacterImg

class FakeCharacterRepository(CharacterRepository):
    def __init__(self):
        self._characters = []
        self._next_id = 1
    
    def save(self, character: Character) -> None:
        self._characters.append(character)

    def all(self) -> list[Character]:
        return list(self._characters)
    
    def get_by_id(self, id: int) -> Character | None:
        for c in self._characters:
            if id == self._next_id:
                return c
        return None
    
    def update(self, id: int, character: Character) -> Character | None:
        if 0 < id <= len(self._characters):
            self._characters[id - 1] = character
            return character
        return None
    
    def delete(self, id: int) -> bool:
        return True


class TestUpdateCharacter:
    def test_update_character_success(self) -> None:
        character_repository = FakeCharacterRepository()

        original = Character(
            name="Tanjiro Kamado",
            state="alive",
            img=CharacterImg(value="https://example.com/tanjiro.jpg")
        )
        character_repository.save(original)

        result = UpdateCharacter(character_repository).execute(
            UpdateCharacterCommand(
                id=1,
                name="Tanjiro Kamado",
                state="dead",
                img="https://example.com/tanjiro-v2.jpg"
            )
        )

        assert result is not None
        assert result.name() == "Tanjiro Kamado"
        assert result.state() == "dead"

    def test_update_character_not_found(self) -> None:
        character_repository = FakeCharacterRepository()

        result = UpdateCharacter(character_repository).execute(
            UpdateCharacterCommand(
                id=999,
                name="Tanjiro Kamado",
                state="alive",
                img="https://example.com/tanjiro.jpg"
            )
        )
        
        assert result is None