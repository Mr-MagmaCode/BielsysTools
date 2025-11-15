# ImportCodefiles

Small helper utilities to find source files and generate LaTeX snippets which include
source code using the minted package (\inputminted).

This folder contains `filesForLatex.py` — a tiny tool to scan a directory tree for
source files (C/C++/Python and friends) and generate LaTeX fragments that include
those files with a sensible language mapping for minted/Pygments.

## Features

- Recursively find source files while skipping hidden files and directories (those starting with `_` or `.`).
- Configurable set of extensions to search.
- Generate LaTeX snippets with `\inputminted{<lang>}{<folder>/<file>}` entries.
- Allow a global minted language override or per-extension language mapping.
- CLI support and programmatic API for integration in other scripts.

## Files

- `filesForLatex.py` — main module with functions:
- `find_source_files(root_dir, exts=..., exclude_prefixes=..., exclude_files=None)`
- `generate_latex_for_files(file_list, section_title=..., folder_in_latex=..., language_override=None, ext_lang_map=None)`
- `print_latex_for_files(...)`, `save_latex_to_file(...)`, and a simple CLI entrypoint.
- `tests/test_filesForLatex.py` — unit tests verifying key behavior.

## Quick usage (programmatic)

Example: generate LaTeX for a list of files from Python:

```python
from filesForLatex import find_source_files, generate_latex_for_files

root = 'path/to/project'
files = find_source_files(root)
latex = generate_latex_for_files(files, section_title='Code Appendix', folder_in_latex='Kode')
print(latex)
```

This prints LaTeX with `\section{Code Appendix}` (if a non-empty section is provided)
and a page + subsection + `\inputminted{...}{...}` block for each file.

## CLI usage

Run the module as a script to print or save a `.tex` fragment:

```bash
python filesForLatex.py            # prints LaTeX for files found next to the script
python filesForLatex.py -o out     # saves to out.tex

# Example with options
python filesForLatex.py --folder Kode --section "Code" --language-override cpp --lang-map ".h=cpp,.py=python3"
```

CLI options summary (from the script):

- `-o, --output` : Output .tex file (if omitted, LaTeX is printed to stdout).
- `--folder` : Folder name used inside LaTeX `\inputminted{...}{<folder>/<file>}` (default: `Kode`).
- `--section` : Section title to add at top (empty = no section).
- `--language-override` : Force the minted language for all files.
- `--lang-map` : Comma-separated per-extension mapping, e.g. `.h=cpp,.py=python`.

Notes on `--lang-map`: keys may be provided with or without the leading dot. The script
normalizes keys to begin with `.`.

## Per-extension mapping and detection

The library contains a small internal extension-to-language map used when no global
override is provided. Example defaults include `.py -> python`, `.c/.h -> c`, `.cpp/.hpp -> cpp`.

You can provide `ext_lang_map` programmatically to `generate_latex_for_files` or
via the CLI with `--lang-map` to override specific extensions.

## Tests

There are unit tests in `tests/test_filesForLatex.py` that validate:

- `find_source_files` respects excluded prefixes and returns relative paths.
- `generate_latex_for_files` detects languages correctly and respects overrides.

Run tests with pytest from the `ImportCodefiles` directory or repository root:

```bash
pytest -q
```

## Developer notes

- The script intentionally filters directories and files that start with `_` or `.`.
- By default it searches for extensions `(.c, .cpp, .h, .hpp, .py)`; adapt by calling `find_source_files` with a custom `exts` tuple.
- The generated LaTeX assumes you have `\usepackage{minted}` in your LaTeX preamble and that you run `pdflatex`/`xelatex`/`lualatex` with `-shell-escape` when required.

## License

Provided as-is.
