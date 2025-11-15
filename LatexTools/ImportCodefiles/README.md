# filesForLatex

A small Python utility to generate LaTeX code (minted) that includes source files from a project directory. It's useful for creating appendices or code listings in reports and theses.

---

## Overview

`filesForLatex.py` scans a directory tree for source files (C, C++, headers, and Python), filters out undesired files and folders, and generates LaTeX snippets that include those files using the `minted` package. The output can be printed to stdout or saved as a `.tex` file.

## Features

- Recursively finds source files with extensions: `.c`, `.cpp`, `.h`, `.hpp`, `.py`.
- Excludes files and directories that begin with `_` or `.` and items named `cmake` by default.
- Optionally skip specific files via `exclude_files` when calling the function programmatically.
- Generates LaTeX with per-file `\subsection`, `\label`, and `\newpage` separators.
- Auto-detects a sensible minted/Pygments language per file extension and uses `\inputminted{<lang>}{...}` for each file.
- Supports a global `--language-override` CLI option (or `language_override` function argument) to force a single language for all files.

## Requirements

- Python 3.6+
- For rendering the generated `.tex` using `minted` you'll need LaTeX with the `minted` package and `pygments` installed. Example:

```bash
# On Debian/Ubuntu
sudo apt install texlive-latex-recommended texlive-latex-extra python3-pygments
```

When compiling the final LaTeX document that uses `minted`, remember to pass `-shell-escape` to `pdflatex` or `xelatex`.

### Recommended `minted` configuration

If you customize `minted` options in your LaTeX preamble, you can set per-language options. Here's the custom block you mentioned (works if your LaTeX environment recognizes the language name you use):

```tex
\usepackage{minted}
\setminted[C++]{
  breaklines=true,
  mathescape=true,
  fontsize=\footnotesize,
  linenos=true,
  numberblanklines=false,
  frame=leftline,
  framerule=0.8pt,
  style=tango
}
```

Note: minted uses Pygments lexers for highlighting. The script maps common extensions to typical minted names by default (mapping examples below). If your LaTeX setup expects a different name (e.g. `C++` instead of `cpp`), you can either use the `--language-override` flag or set per-language options in the LaTeX preamble using `\setminted[<name>]{...}`.

Default mapping used by the script (extension -> minted name):

- `.py` -> `python`
- `.c` -> `c`
- `.h` -> `c` (changeable; see notes)
- `.cpp`, `.cc`, `.cxx`, `.hpp` -> `cpp`
- unknown extensions -> `text`

If your repository uses `.h` for C++ headers, you may prefer mapping `.h` to `cpp`; see "Notes" below.

## Usage

Print LaTeX to stdout from the script folder:

```bash
python3 filesForLatex.py
```

Save output to a `.tex` file, set a custom folder name used in the LaTeX `\inputminted` paths, and force a single minted language for all files:

```bash
python3 filesForLatex.py -o code_appendix.tex --folder Kode --section "Appendix: Source Code" --language-override "C++"
```

When no override is provided, the script will auto-detect language per file and emit lines like:

```tex
\inputminted{cpp}{Kode/src/main.cpp}
\inputminted{python}{Kode/scripts/util.py}
```

When `--language-override "C++"` is used, every `\inputminted` will use `C++` as the language key.

## Example (snippet produced)

Detected-language output:

```tex
\section{Appendix: Source Code}
\newpage
\label{sec:src_main_cpp}
\subsection{src/main.cpp}
\inputminted{cpp}{Kode/src/main.cpp}
```

Override example:

```tex
\inputminted{C++}{Kode/src/main.cpp}
```

## API (for programmatic use)

Primary functions available in `filesForLatex.py`:

- `find_source_files(root_dir, exts=..., exclude_prefixes=..., exclude_files=None)`
  - Returns a sorted list of relative file paths matching the configured extensions and filters.

- `generate_latex_for_files(file_list, section_title="Kode vedlegg", folder_in_latex="Kode", language_override=None)`
  - Returns a string containing the assembled LaTeX code for the provided files. If `language_override` is provided, it will be used verbatim for every `\inputminted{...}`.

- `print_latex_for_files(file_list, section_title=None, folder_in_latex="Kode", language_override=None)`
  - Prints the generated LaTeX to stdout.

- `save_latex_to_file(file_list, output_file, section_title=None, folder_in_latex="Kode", language_override=None)`
  - Saves the generated LaTeX to `output_file` (adds `.tex` if missing) and returns `True` on success.

## Tests

I added a small pytest test file to validate file discovery and language mapping:

```
LatexTools/ImportCodefiles/tests/test_filesForLatex.py
```

To run the tests locally:

```bash
# Install pytest if you don't have it
python3 -m pip install --user pytest

# Run the tests
pytest -q LatexTools/ImportCodefiles/tests/test_filesForLatex.py
```

The tests check that `find_source_files` respects excludes (files starting with `_` or `.` are ignored) and that `generate_latex_for_files` selects appropriate minted languages and respects `language_override`.

## Notes and tips

- The default `.h -> c` mapping is conservative. If your project uses `.h` headers for C++, change the mapping in `filesForLatex.py` (`.h` -> `cpp`) or use `--language-override` when generating LaTeX.
- If your LaTeX setup expects `C++` (capitalization or alternate name), use `--language-override "C++"` or set `\setminted[C++]{...}` in your preamble.
- To include only a subset of files, call `find_source_files` programmatically and pass a curated list to `generate_latex_for_files`.

## License

This repository is provided as-is. Add a license file if you wish to specify usage terms.

---

If you'd like, I can change the default `.h` mapping to `cpp`, add a per-extension CLI mapping option, or include a small helper that copies discovered source files into the LaTeX `Kode` folder before generation.
