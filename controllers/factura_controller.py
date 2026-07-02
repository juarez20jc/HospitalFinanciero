class FacturaController:
    def __init__(self, repo):
        self.repo = repo

    def listar(self):
        return self.repo.listar_facturas()

    def detalle(self, invoice_id):
        return self.repo.detalle_factura(invoice_id)

    def pendientes(self):
        return self.repo.facturas_pendientes()

    def generar_desde_cita(self, id_reserva, user):
        self.repo.generar_factura_desde_cita(id_reserva, user)

    def anular(self, data, user):
        self.repo.anular_factura(data, user)
