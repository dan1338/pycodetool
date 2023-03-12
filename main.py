#!/usr/bin/env python3

from dataclasses import dataclass
import re

@dataclass
class Sexpr:
    kind: str
    range: slice
    children: list

    def text(self, s):
        return s[self.range]

    def fields(self):
        return list(map(lambda x: x[0], self.children))

    def __getitem__(self, i):
        match i:
            case int(i):
                return list(map(lambda x: x[1], self.children))[i]
            case str(s):
                return dict(self.children)[s]

    def all_children(self):
        for (_, child) in self.children:
            yield child
            yield from child.all_children()

def make_sexpr(s):
    re_open = re.compile('\s*\((\w+) \[(\d+):(\d+)\]')
    re_field = re.compile(' (\w+): ')

    if m := re_open.match(s):
        # Skip match
        s = s[m.end():]

        # Make sexpr
        kind, start, end = m.groups()

        class ChildConsumer:
            def __init__(self, s):
                self.s = s
            def __iter__(self):
                s = self.s
                while s[0] != ')':
                    # By default field is null
                    field = None

                    # Try parsing the field
                    if m := re_field.match(s):
                        field = m.groups()[0]
                        s = s[m.end():]
                    
                    expr, s = make_sexpr(s)
                    yield field, expr
                self.s = s[1:]

        consumer = ChildConsumer(s)
        children = list(consumer)
        expr = Sexpr(kind, slice(int(start), int(end)), children)

        return (expr, consumer.s)

    raise Exception(f"Could not match sexpr: \"{s:.40s}\"...")

import sys
from pathlib import Path

sexp_path = Path(sys.argv[1])
source_path = Path(sys.argv[2])

source = source_path.read_text()
root, _ = make_sexpr(sexp_path.read_text())

for (field, child) in root.children:
    if 'function' in child.kind:
        print(field, child.kind)
        print(source[child.range])

