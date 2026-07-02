from dataclasses import dataclass


@dataclass
class DetalleFactura:
    descripcion: str
    cantidad: int
    precio_unitario: float
    subtotal: float
