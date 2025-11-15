import importlib.util
import sys
from pathlib import Path
import os

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / 'filesForLatex.py'


def load_module():
    spec = importlib.util.spec_from_file_location(
        'filesForLatex', str(MODULE_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_find_source_files_respects_excludes(tmp_path):
    # Create a directory structure with files, some of which should be excluded
    root = tmp_path / 'proj'
    (root / 'sub').mkdir(parents=True)
    # included files
    f1 = root / 'sub' / 'good.c'
    f1.write_text('int main(){}')
    f2 = root / 'keep.py'
    f2.write_text('print(1)')
    # excluded by starting with _ and .
    f3 = root / '_secret.c'
    f3.write_text('')
    f4 = root / '.hidden.py'
    f4.write_text('')

    mod = load_module()
    found = mod.find_source_files(str(root))
    # should find good.c and keep.py only (relative paths)
    assert sorted(found) == sorted(
        [os.path.relpath(str(f1), str(root)), os.path.relpath(str(f2), str(root))])


def test_generate_latex_language_mapping_and_override():
    mod = load_module()
    files = ['src/main.cpp', 'script.py', 'include/header.h', 'utils.c']
    out = mod.generate_latex_for_files(
        files, section_title='Test', folder_in_latex='Kode')
    assert '\\inputminted{cpp}{Kode/src/main.cpp}' in out
    assert '\\inputminted{python}{Kode/script.py}' in out
    assert '\\inputminted{c}{Kode/include/header.h}' in out
    assert '\\inputminted{c}{Kode/utils.c}' in out

    # Now test override
    out2 = mod.generate_latex_for_files(
        files, section_title='Test', folder_in_latex='Kode', language_override='C++')
    # All inputminted occurrences should use the override 'C++'
    assert out2.count('\\inputminted{C++}') == len(files)
