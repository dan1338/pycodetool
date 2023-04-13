from dataclasses import dataclass
from utils import *
import re

@dataclass
class Sexp:
    kind: str
    range: slice
    children: list

    def __repr__(self):
        return f'Sexp({self.kind}, {self.fields()})'

    def __getitem__(self, i):
        match i:
            case slice(start=start, stop=stop, step=step):
                return lmap(snd, self.children[start:stop:step])
            case int(i):
                return snd(self.children[i])
            case str(s):
                return dict(self.children)[s]

    def fields(self):
        return lmap(fst, self.children)

    def recurse_field(self, field_, **kwargs):
        map_ = kwargs.get('map', lambda x: x)
        for (field, child) in self.children:
            if field == field_:
                yield child
                yield from child.recurse_field(field_, **kwargs)

    def all(self, **kwargs):
        field_ = kwargs.get('field')
        kind_ = kwargs.get('kind')
        map_ = kwargs.get('map', lambda x: x)
        for (field, child) in self.children:
            if field_ and field != field_:
                yield from child.all(**kwargs)
                continue
            if kind_ and child.kind != kind_:
                yield from child.all(**kwargs)
                continue
            yield map_((field, child))
            yield from child.all(**kwargs)

def make_sexp(s):
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
                    
                    expr, s = make_sexp(s)
                    yield field, expr
                self.s = s[1:]

        consumer = ChildConsumer(s)
        children = list(consumer)
        expr = Sexp(kind, slice(int(start), int(end)), children)

        return (expr, consumer.s)

    raise Exception(f"Could not match sexpr: \"{s:.40s}\"...")

