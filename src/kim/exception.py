class ForbiddenFilename(Exception):
    def __init__(self, category: object) -> None:
        """Ensure the category is a valid filename

        Args:
            category (object): category will become category.py
        """
        msg = f"{category} is not a valid name for a file"
        super().__init__(msg)

class ForbiddenVariableName(Exception):
    def __init__(self, name: object) -> None:
        """Ensure the name is a valid variable name

        Args:
            name (object): name will become `name = ...`
        """
        msg = f"{name} is not a valid name for a variable"
        super().__init__(msg)
