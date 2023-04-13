from sexp import *
from dataclasses import dataclass
from pathlib import Path
import sexpgen
from io import StringIO

@dataclass(frozen=True)
class SourceFile:
    path: Path
    text: str
    root: Sexp

    def ext(self):
        return self.path.suffix

    def __repr__(self):
        return f'SourceFile({self.path})'

def make_source_file(path, lang=None):
    path = Path(path)
    text = path.read_text()

    # create .sexp directory for this file
    sexp_path = '.sexp' / path
    sexp_path.parents[0].mkdir(exist_ok=True, parents=True)

    # generate and parse the S-expression
    ss = StringIO()
    if lang:
        sexpgen.from_string(text, lang, ss)
    else:
        sexpgen.from_file(path, ss)
    root, _ = make_sexp(ss.getvalue())

    return SourceFile(path, text, root)

