# -*- coding: utf-8 -*-

"""Test Markdown parser and reader."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

from ...core.format_manager import convert
from ...utils.utils import _diff
from ._utils import (_test_reader, _test_writer, _read_test_file)


#------------------------------------------------------------------------------
# Test Markdown parser
#------------------------------------------------------------------------------

def _test_ipymd_reader(basename, ignore_notebook_meta=False):
    """Check that (test cells) and (test contents ==> cells) are the same."""
    converted, expected = _test_reader(basename, 'ipymd',
                                       ignore_notebook_meta)
    assert converted == expected


def _test_ipymd_writer(basename):
    """Check that (test contents) and (test cells ==> contents) are the same.
    """
    converted, expected = _test_writer(basename, 'ipymd')
    assert _diff(converted, expected) == ''


def _test_ipymd_ipymd(basename):
    """Check that the double conversion is the identity."""

    contents = _read_test_file(basename, 'ipymd')
    cells = convert(contents, from_='ipymd')
    converted = convert(cells, to='ipymd')

    assert _diff(contents, converted) == ''


def test_ipymd_reader():
    _test_ipymd_reader('ex1')
    _test_ipymd_reader('ex2')
    _test_ipymd_reader('ex3')
    _test_ipymd_reader('ex4', ignore_notebook_meta=False)


def test_markdown_writer():
    _test_ipymd_writer('ex1')
    _test_ipymd_writer('ex2')
    _test_ipymd_writer('ex3')
    _test_ipymd_writer('ex4')


def test_ipymd_ipymd():
    _test_ipymd_ipymd('ex1')
    _test_ipymd_ipymd('ex2')
    _test_ipymd_ipymd('ex3')
    _test_ipymd_ipymd('ex4')


def test_decorator():
    markdown = '\n'.join(('```python-cell',
                          '@decorator',
                          'def f():',
                          '    """Docstring."""',
                          '',
                          '    # Comment.',
                          '    pass',
                          '',
                          '    # Comment.',
                          '    pass',
                          '    pass',
                          '```',
                          '',
                          '```output-cell',
                          'blah',
                          'blah',
                          '```'))

    cells = convert(markdown, from_='ipymd')

    assert '...' not in cells[0]['input']
    assert cells[0]['output'] == 'blah\nblah'

    markdown_bis = convert(cells, to='ipymd')
    assert _diff(markdown, markdown_bis) == ''
