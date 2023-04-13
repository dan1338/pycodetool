from dataclasses import dataclass
from source_file import make_source_file
from sexp import *
from pathlib import Path
from functools import partial

@dataclass(frozen=True)
class Lang:
    name: str
    exts: list

PY_LANG = Lang('python', exts=['.py'])
C_LANG = Lang('c', exts=['.c', '.h'])

class Project:
    def __init__(self, path, lang):
        self.path = Path(path)
        self.lang = lang
        #make_source_file = partial(make_source_file, lang=lang.name)
        self.files = lmap(make_source_file, self.find_files())

    def find_files(self):
        for ext in self.lang.exts:
            yield from self.path.rglob(f'*{ext}')

