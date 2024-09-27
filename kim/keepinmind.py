import shelve
import os
import importlib
import importlib.util
import kim
import sys

def reload_module(module_name):
    """
    Recharge le module pour mettre à jour le cache après une modification.
    """
    if module_name in sys.modules:
        # Supprime le module du cache
        del sys.modules[module_name]

    # Recharge le module
    importlib.import_module(module_name)
    return sys.modules[module_name]

class KeepInMind:
    def __init__(self) -> None:
        self.__rootpath__ = "kim/root"
        self.__rootmodule__ = self.__rootpath__.replace("/", ".")
        self.__shelvefolder__ = "kim/.memory"
        self.__vault__ = self.__shelvefolder__ + "/memory"
        self.__importfile__ = self.__rootpath__ + "/__init__.py"
        self.__ext__ = ".py"
    def _refresh_root(self):
        os.makedirs(self.__rootpath__, exist_ok=True)
        with shelve.open(self.__vault__) as coffre:
            for name, value in list(coffre[self.__rootpath__].items()):
                with open(self.__rootpath__ + "/" + name + self.__ext__, "w") as f:
                    for name_, value_ in list(value.items()):
                        f.write("%s = %s\n" % (name_, repr(value_)))

    def _refresh_init(self):
        with shelve.open(self.__vault__) as coffre:
            with open(self.__importfile__, "w") as f:
                for name in list(coffre[self.__rootpath__].keys()):
                    f.write("from .%s import *\n" % (name))

    def _add_to_cache(self, category, name, value):
        file_path = f"{self.__rootpath__}/{category}{self.__ext__}"
        module_name = f"{self.__rootmodule__}.{category}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        alias_name = f"kim.{category}"
        sys.modules[alias_name] = module
        setattr(kim, category, module)
        setattr(module, name, value)

    def _del_from_cache(self, category=None):
        module = f"kim.{category}" if category is not None else "kim"
        module = importlib.import_module(module)
        for attr in dir(module):
            if not attr.startswith("__"):
                delattr(module, attr)
        if module in sys.modules:
            del sys.modules[module]


class CreateOrUpdate(KeepInMind):
    def __init__(self, category, name, value) -> None:
        super().__init__()
        os.makedirs(self.__shelvefolder__, exist_ok=True)
        with shelve.open(self.__vault__) as coffre:
            if self.__rootpath__ not in coffre:
                coffre[self.__rootpath__] = {}
            squeleton = coffre[self.__rootpath__]
            if category not in squeleton:
                squeleton[category] = {}
            squeleton[category][name] = value
            coffre[self.__rootpath__] = squeleton
        self._refresh_root()
        self._refresh_init()
        self._add_to_cache(category, name, value)


class Remove(KeepInMind):
    def __init__(self, category=None, all=False) -> None:
        super().__init__()
        if all:
            with shelve.open(self.__vault__) as coffre:
                coffre[self.__rootpath__] = {}
            for file_path in os.listdir(self.__rootpath__):
                if not file_path.endswith('__init__.py') and file_path[-3:] == self.__ext__:
                    os.remove(self.__rootpath__ + "/" + file_path)
        else:
            with shelve.open(self.__vault__) as coffre:
                vault = coffre[self.__rootpath__]
                del vault[category]
                coffre[self.__rootpath__] = vault
                os.remove(self.__rootpath__ + "/" + category+self.__ext__)

        self._refresh_root()
        self._refresh_init()
        self._del_from_cache(category=category)



            

 

