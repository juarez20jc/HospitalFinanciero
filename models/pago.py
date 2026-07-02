from dataclasses import dataclass


@dataclass
class Pago:
    id_factura: int
    tipo_pago: str
    monto: float
