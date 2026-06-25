from dataclasses import dataclass
import validators
from src.characters.domain.exception import CharacterImgNotValid

@dataclass(frozen=True, kw_only=True)
class CharacterImg:
    value:str
    
    def __post_init__(self) ->None:
        if not validators.url(self.value):
            raise CharacterImgNotValid