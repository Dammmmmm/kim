class Root():
    def __init__(self) -> None:
        self.path = "kim/root"
        self.module = self.path.replace("/", ".")

class Vault():
    def __init__(self) -> None:
        self.folder = "kim/.memory"
        self.file = self.folder + "/memory"
