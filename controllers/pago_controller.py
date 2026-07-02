class PagoController:
    def __init__(self, repo):
        self.repo = repo

    def listar_pendientes(self):
        return self.repo.facturas_para_pago()

    def registrar(self, data, user):
        self.repo.registrar_pago(data, user)

    def caja_diaria(self):
        return self.repo.caja_diaria()
