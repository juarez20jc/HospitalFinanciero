from dataclasses import dataclass


@dataclass
class Paciente:
    dni: str
    nombres: str
    apellidos: str
    telefono: str
    email: str = ""
