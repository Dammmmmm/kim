class ForbiddenFilename(Exception):
    def __init__(self, category: object) -> None:
        msg = f"{category} is not a valid name for a file"
        super().__init__(msg)

class ForbiddenVariableName(Exception):
    def __init__(self, name: object) -> None:
        msg = f"{name} is not a valid name for a variable"
        super().__init__(msg)
