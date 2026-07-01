from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.characters.domain.models import Character
from src.characters.application.create_character import CreateCharacter, CreateCharacterCommand
from src.characters.application.get_all_character import GetAllCharacters
from src.characters.application.get_character_by_id import GetCharacterById
from src.characters.application.update_character import UpdateCharacter, UpdateCharacterCommand
from src.characters.application.delete_character import DeleteCharacter, DeleteCharacterCommand
from src.characters.infraestructure.repositories import SQLModelCharacterRepository

router = APIRouter()

class CharacterPayload(BaseModel):
    name: str
    state: str
    img: str

class CharacterResponse(BaseModel):
    id: int | None
    name: str
    state: str
    img: str

    @classmethod
    def from_domain(cls, character: Character) -> "CharacterResponse":
        return cls(
            id=character.id(),
            name=character.name(),
            state=character.state(),
            img=character.img().value
        )

@router.get("/characters/")
def get_all_characters() -> list[CharacterResponse]:
    characters = GetAllCharacters(SQLModelCharacterRepository()).execute()
    return [CharacterResponse.from_domain(c) for c in characters]

@router.get("/characters/{id}")
def get_character_by_id(id: int) -> CharacterResponse:
    character = GetCharacterById(SQLModelCharacterRepository()).execute(id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return CharacterResponse.from_domain(character)

@router.post("/characters/")
def create_character(payload: CharacterPayload) -> CharacterResponse:
    character = CreateCharacter(SQLModelCharacterRepository()).execute(
        CreateCharacterCommand(
            name=payload.name,
            state=payload.state,
            img=payload.img
        )
    )
    return CharacterResponse.from_domain(character)

@router.put("/characters/{id}")
def update_character(id: int, payload: CharacterPayload) -> CharacterResponse:
    character = UpdateCharacter(SQLModelCharacterRepository()).execute(
        UpdateCharacterCommand(
            id=id,
            name=payload.name,
            state=payload.state,
            img=payload.img
        )
    )
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return CharacterResponse.from_domain(character)

class DeleteResponse(BaseModel):
    message: str

@router.delete("/characters/{id}")
def delete_character(id: int) -> DeleteResponse:
    deleted = DeleteCharacter(SQLModelCharacterRepository()).execute(
        DeleteCharacterCommand(id=id)
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Character not found")
    return DeleteResponse(message="Character deleted successfully")