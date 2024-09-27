from .util.path import Vault, Root
from .util.verify import is_valid_filename, is_valid_variable_name
from .util.exception import ForbiddenFilename, ForbiddenVariableName
import shelve
import os
import importlib
import importlib.util
import kim
import sys

class KeepInMind:
    def __init__(self) -> None:
        self.__root__ = Root()
        self.__vault__ = Vault()
        self.__importfile__ = self.__root__.path + "/__init__.py"
        self.__ext__ = ".py"
        self._refresh_init()

    def _refresh_root(self):
        os.makedirs(self.__root__.path, exist_ok=True)
        with shelve.open(self.__vault__.file) as coffre:
            for name, value in list(coffre[self.__root__.path].items()):
                with open(self.__root__.path + "/" + name + self.__ext__, "w") as f:
                    for name_, value_ in list(value.items()):
                        f.write("%s = %s\n" % (name_, repr(value_)))

    def _refresh_init(self):
        with shelve.open(self.__vault__.file) as coffre:
            with open(self.__importfile__, "w") as f:
                for name in list(coffre[self.__root__.path].keys()):
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


class CreateOrUpdate(KeepInMind):
    def __init__(self, category, name, value) -> None:
        if not is_valid_filename(category):
            raise ForbiddenFilename(category)
        if not is_valid_variable_name(name):
            raise ForbiddenVariableName(name)
        super().__init__()
        os.makedirs(self.__vault__.folder, exist_ok=True)
        with shelve.open(self.__vault__.file) as coffre:
            if self.__root__.path not in coffre:
                coffre[self.__root__.path] = {}
            squeleton = coffre[self.__root__.path]
            if category not in squeleton:
                squeleton[category] = {}
            squeleton[category][name] = value
            coffre[self.__root__.path] = squeleton
        self._refresh_root()
        self._refresh_init()
        self._add_to_cache(category, name, value)


class Remove(KeepInMind):
    def __init__(self, category, name=None) -> None:
        super().__init__()
        if name is None:
            with shelve.open(self.__vault__.file) as coffre:
                vault = coffre[self.__root__.path]
                del vault[category]
                coffre[self.__root__.path] = vault
            os.remove(self.__root__.path + "/" + category + self.__ext__)
            self._refresh_root()
            self._refresh_init()
            self._del_from_cache(category)
        else:
            with shelve.open(self.__vault__.file) as coffre:
                vault = coffre[self.__root__.path]
                del vault[category][name]
                coffre[self.__root__.path] = vault
            self._refresh_root()
            self._refresh_init()
            importlib.reload(kim)
            importlib.reload(importlib.import_module(self.__root__.module + "." + category))


class Clear(KeepInMind):
    def __init__(self) -> None:
        super().__init__()
        with shelve.open(self.__vault__.file) as coffre:
            coffre[self.__root__.path] = {}
        for file_path in os.listdir(self.__root__.path):
            if not file_path.endswith('__init__.py') and file_path[-3:] == self.__ext__:
                os.remove(self.__root__.path + "/" + file_path)
        
        self._refresh_root()
        self._refresh_init()
        self._clear_cache()
