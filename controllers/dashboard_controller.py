class DashboardController:
    def __init__(self, repo):
        self.repo = repo

    def summary(self):
        return self.repo.dashboard()
