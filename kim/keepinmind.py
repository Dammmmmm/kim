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
    def _update_root(self):
        os.makedirs(self.__rootpath__, exist_ok=True)
        #for f in os.listdir(self.__rootpath__):
        #    os.remove(self.__rootpath__+"/"+f)
        with shelve.open(self.__vault__) as coffre:
            for name, value in list(coffre[self.__rootpath__].items()):
                with open(self.__rootpath__ + "/" + name + self.__ext__, "w") as f:
                    for name_, value_ in list(value.items()):
                        f.write("%s = %s\n" % (name_, repr(value_)))

    def _refresh_import(self):
        with shelve.open(self.__vault__) as coffre:
            with open(self.__importfile__, "w") as f:
                for name in list(coffre[self.__rootpath__].keys()):
                    f.write("from .%s import *\n"%(name))

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
        self._update_root()
        self._refresh_import()
        importlib.reload(importlib.import_module(f'{self.__rootmodule__}'))
        importlib.reload(importlib.import_module(f'{self.__rootmodule__}.{category}'))
        file_path = f"{self.__rootpath__}/{category}{self.__ext__}"
        module_name = f"{self.__rootmodule__}.{category}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        alias_name = f"kim.{category}"
        sys.modules[alias_name] = module
        import kim
        setattr(kim, category, module)
        setattr(module, name, value)

class Remove(KeepInMind):
    def __init__(self, all) -> None:
        super().__init__()
        if all:
            with shelve.open(self.__vault__) as coffre:
                coffre[self.__rootpath__] = {}
            for file in os.listdir(self.__rootpath__):
                if file[-3:] == self.__ext__:
                    os.remove(self.__rootpath__ + "/" + file)
            
            self._update_root()
            self._refresh_import()
            importlib.reload(kim)
            importlib.reload(importlib.import_module(f'{self.__rootmodule__}'))
 


            

 

