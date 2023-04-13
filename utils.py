from functools import partial

lmap = lambda f, x: list(map(f, x))
lfilter = lambda f, x: list(filter(f, x))

ifirst = lambda x: list(x)[0]
ilast = lambda x: list(x)[-1]

fst = lambda x: x[0]
snd = lambda x: x[1]

eq = lambda a, b: a == b
neq = lambda a, b: a != b
ge = lambda a, b: a > b
le = lambda a, b: a < b

