import ast

from parameterized import parameterized

from flake8_f_string import (
    Plugin,
    FS100,
)


def results(s):
    return {'{}:{}: {}'.format(*r) for r in Plugin(ast.parse(s)).run()}


@parameterized.expand([
    "f'{abs(1)}'",
    "f'{len(foo)}'",
    "f'{foo()}'",
    "f'{Foo.bzz()}'",
])
def test_fs_100_with_invalid(value):
    assert results(value) == {f'1:0: {FS100}'}


@parameterized.expand([
    "",
    "f''",
    "f'{foo}'",
    "f'{foo.bzz}'",
])
def test_fs_100_with_valid(value):
    assert results(value) == set()
