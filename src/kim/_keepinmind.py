import importlib
import importlib.util
import os
import shelve
import sys

import kim

from typing import Any, Dict

from kim._utils.path import _Vault, _Root
from kim._utils.verify import _is_valid_filename, _is_valid_variable_name
from kim.exception import ForbiddenFilename, ForbiddenVariableName


class _KeepInMind:
    def __init__(self) -> None:
        self.__root__ = _Root()
        self.__vault__ = _Vault()
        self.__importfile__ = self.__root__.path + "/__init__.py"
        self.__ext__ = ".py"
        self._refresh_init()

    def _refresh_root(self):
        os.makedirs(self.__root__.path, exist_ok=True)
        with shelve.open(self.__vault__.file) as vault:
            for name, value in list(vault[self.__root__.path].items()):
                with open(self.__root__.path + "/" + name + self.__ext__, "w") as f:
                    for name_, value_ in list(value.items()):
                        f.write("%s = %s\n" % (name_, repr(value_)))

    def _refresh_init(self):
        with shelve.open(self.__vault__.file) as vault:
            with open(self.__importfile__, "w") as f:
                for name in list(vault[self.__root__.path].keys()):
                    f.write("from .%s import *\n" % (name))

    def _add_to_cache(self, category, name, value):
        file_path = f"{self.__root__.path}/{category}{self.__ext__}"
        module_name = f"{self.__root__.module}.{category}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        alias_name = f"kim.{category}"
        sys.modules[alias_name] = module
        setattr(kim, category, module)
        setattr(module, name, value)

    def _clear_cache(self):
        module = "kim"
        module = importlib.import_module(module)
        for attr in dir(module):
            if not attr.startswith("__"):
                delattr(module, attr)
        if module in sys.modules:
            del sys.modules[module]

    def _del_from_cache(self, category):
        module = importlib.import_module("kim")
        delattr(module, category)
        if module in sys.modules:
            del sys.modules[module]


class CreateOrUpdate(_KeepInMind):
    def __init__(self, category: str, name: str, value: Any) -> None:
        """Create or update a variable, that you can use by calling : kim.category.name

        Args:
            category (str): a category for your variable
            name (str): the name of your variable
            value (Any): whetever it's equal to

        Raises:
            ForbiddenFilename: category must be usable as a filename
            ForbiddenVariableName: name must be usable as a python variable name
        """
        if not _is_valid_filename(category):
            raise ForbiddenFilename(category)
        if not _is_valid_variable_name(name):
            raise ForbiddenVariableName(name)
        super().__init__()
        os.makedirs(self.__vault__.folder, exist_ok=True)
        with shelve.open(self.__vault__.file) as vault:
            if self.__root__.path not in vault:
                vault[self.__root__.path] = {}
            squeleton = vault[self.__root__.path]
            if category not in squeleton:
                squeleton[category] = {}
            squeleton[category][name] = value
            vault[self.__root__.path] = squeleton
        self._refresh_root()
        self._refresh_init()
        self._add_to_cache(category, name, value)


class Remove(_KeepInMind):
    def __init__(self, category:str, name:str=None) -> None:
        """Remove either a whole category or a variable in category (no undo)

        Args:
            category (str): the target category
            name (str, optional): the name of the variable to delete, if None the 
            whole category will be deleted. Defaults to None.
        """
        super().__init__()
        if name is None:
            with shelve.open(self.__vault__.file) as vault:
                vault = vault[self.__root__.path]
                del vault[category]
                vault[self.__root__.path] = vault
            os.remove(self.__root__.path + "/" + category + self.__ext__)
            self._refresh_root()
            self._refresh_init()
            self._del_from_cache(category)
        else:
            with shelve.open(self.__vault__.file) as vault:
                vault = vault[self.__root__.path]
                del vault[category][name]
                vault[self.__root__.path] = vault
            self._refresh_root()
            self._refresh_init()
            importlib.reload(kim)
            importlib.reload(importlib.import_module(self.__root__.module + "." + category))


class Clear(_KeepInMind):
    def __init__(self) -> None:
        """
        Clear any remaining variables created with CreateOrUpdate (no undo)
        """
        super().__init__()
        with shelve.open(self.__vault__.file) as vault:
            vault[self.__root__.path] = {}
        for file_path in os.listdir(self.__root__.path):
            if not file_path.endswith('__init__.py') and file_path[-3:] == self.__ext__:
                os.remove(self.__root__.path + "/" + file_path)
        
        self._refresh_root()
        self._refresh_init()
        self._clear_cache()


def variables_dict() -> Dict[Dict]:
    """Retreive all the variables created with CreateOrUpdate

    Returns:
        Dict: a dictionary of dictionary
    """
    vault_file = _KeepInMind().__vault__.file
    root_path = _KeepInMind().__root__.path
    with shelve.open(vault_file) as vault:
        return_ = vault[root_path]
    return return_
