from dataclasses import dataclass


@dataclass
class Factura:
    numero_factura: str
    subtotal: float
    igv: float
    total: float
    estado_pago: str
