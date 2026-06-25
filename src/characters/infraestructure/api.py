from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.characters.domain.models import Character
from src.characters.domain.exception import CharacterImgNotValid
from src.characters.application.create_character import CreateCharacter, CreateCharacterCommand
from src.characters.infraestructure.repository import SQLModelCharacterRepository

router = APIRouter()

class CharacterPayload(BaseModel):
    name: str
    state: str
    img: str
    
class CharacterResponse(BaseModel):
    name: str
    state: str
    img: str
    
    @classmethod
    def from_domain(cls, character: Character) -> "CharacterResponse":
        return cls(
            name=character.name(),
            state=character.state(),
            img=character.img().value
        )


@router.post("/characters/")
def create_character(payload: CharacterPayload) -> CharacterResponse:
    try:
        character = CreateCharacter(SQLModelCharacterRepository()).execute(
            CreateCharacterCommand(
                name=payload.name,
                state=payload.state,
                img=payload.img
            )
        )
    except CharacterImgNotValid as exc:
        raise HTTPException(status_code=400, detail=str(exc) or "Invalid image URL")
    return CharacterResponse.from_domain(character)