class PacienteController:
    def __init__(self, repo):
        self.repo = repo

    def listar(self, q=""):
        return self.repo.listar_pacientes(q)

    def crear(self, data, user):
        self.repo.crear_paciente(data, user)
