class _Root():
    def __init__(self) -> None:
        self.path = "kim/_root"
        self.module = self.path.replace("/", ".")

class _Vault():
    def __init__(self) -> None:
        self.folder = "kim/_memory"
        self.file = self.folder + "/memory"
