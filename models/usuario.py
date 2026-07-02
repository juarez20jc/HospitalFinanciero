from dataclasses import dataclass


@dataclass
class Usuario:
    username: str
    nombres: str
    apellidos: str
    rol: str
