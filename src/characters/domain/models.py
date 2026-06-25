from src.characters.domain.valid_object import CharacterImg

class Character:
    def __init__(self, name: str, state: str, img: CharacterImg | None = None):
        self._name = name
        self._state = state
        self._img = img
        
    @classmethod
    def create(cls,name:str,state:str,img:str)->"Character":
        return cls(name, state,CharacterImg(value=img))

    def name(self) -> str:
        return self._name

    def state(self) -> str:
        return self._state

    def img(self) -> CharacterImg:
        return self._img