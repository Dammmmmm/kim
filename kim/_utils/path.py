import os

class _Root:
    def __init__(self) -> None:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.path = os.path.join(base_path, "_root")
        self.module = "kim._root"

class _Vault:
    def __init__(self) -> None:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.folder = os.path.join(base_path, "_memory")
        self.file = os.path.join(self.folder, "memory")
