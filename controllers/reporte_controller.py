class ReporteController:
    def __init__(self, repo):
        self.repo = repo

    def financieros(self):
        return self.repo.reportes_financieros()

    def exportar_csv(self):
        return self.repo.exportar_reporte_csv()
