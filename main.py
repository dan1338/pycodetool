#!/usr/bin/env python3

from pathlib import Path
from sexp import *
import sys

if len(sys.argv) == 3:
    sexp_path = Path(sys.argv[1])
    source_path = Path(sys.argv[2])
else:
    sexp_path = Path('example/main.sexp')
    source_path = Path('example/main.c')

source = source_path.read_text()
root, _ = make_sexp(sexp_path.read_text())

funcs = list(root.all(kind='function_definition', map=snd))
text = lambda s: source[s.range].strip()
func_symbols = lambda func: map(text, func.all(kind='identifier', map=snd))

