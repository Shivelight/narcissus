from collections import defaultdict
from typing import List, Dict, Callable, TYPE_CHECKING
from importlib.abc import Loader
import os
import importlib.util

from .nlu import Understanding
from .util import get_resource_path

if TYPE_CHECKING:
    from . import Narcissus


_intents = os.path.relpath(get_resource_path(__file__, "intents"))


class IntentManager:
    """Intent manager."""

    def __init__(self, app: "Narcissus", intent_dir: str = _intents):
        self.app = app
        self.intent_dir = intent_dir
        self.intents: Dict[str, List[Callable]] = defaultdict(list)
        self._load_intents()

    def _load_intents(self) -> None:
        modules: List[str] = []
        for dirpath, _, files in os.walk(self.intent_dir):
            for file in files:
                if file.endswith(".py"):
                    path = f"{dirpath.replace(os.sep, '.')}.{file[:-3]}"
                    modules.append(path)
        for module in modules:
            spec = importlib.util.find_spec(module)
            if spec and isinstance(spec.loader, Loader):
                lib = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(lib)
                try:
                    setup = getattr(lib, "setup")
                except AttributeError:
                    print(f"No entry point found in {module}")
                    continue

                try:
                    setup(self)
                except Exception as e:
                    print(e)

    def register_intent(self, name: str, func: Callable) -> None:
        """Used by `Intent` to register itself."""
        self.intents[name].append(func)

    def run_intent(self, data: Understanding) -> bool:
        """Run specified intent."""
        # defaultdict.get here is to avoid creating uneeded key
        # TODO: get rid
        funcs = self.intents.get(data.intent) or self.intents["_default_"]
        for func in funcs:
            if func(data) is False:
                return False
        return True
