from src.characters.domain.value_objects import CharacterImg

class Character:
    def __init__(self, name: str, state: str, img: CharacterImg, id: int | None = None):
        self._id = id
        self._name = name
        self._state = state
        self._img = img

    @classmethod
    # el cls es una referencia a la clase misma, y nos permite crear una instancia de la clase sin necesidad de conocer su nombre exacto. Esto es útil en casos donde queremos crear instancias de subclases de manera dinámica, o cuando queremos mantener el código más flexible y desacoplado.
    # lo que hace este metodo es crear una instancia de la clase Character con los atributos establecidos en los valores proporcionados. Esto nos permite crear characters de manera más sencilla y consistente, sin tener que llamar al constructor directamente.
    #Lo hacemos de esta manera para encapsular la lógica de creación de characters en un solo lugar, lo que facilita el mantenimiento y evolución del código. Además, nos permite cambiar la forma en que se crean los characters sin afectar a otras partes del código que dependen de esta clase.
    def create(cls, name: str, state: str, img: CharacterImg)-> "Character":
        return cls(name, state, img)

    # Esto es para no exponer directamente el atributo privado, y en su lugar proporcionar métodos que devuelvan el valor de esos atributos. Esto nos permite cambiar la implementación interna de la clase sin afectar a otras partes del código que dependen de ella.
    def name(self) -> str:
        return self._name

    def state(self) -> str:
        return self._state

    def img(self) -> "CharacterImg":
        return self._img
    
    def id(self) -> int | None:
        return self._id