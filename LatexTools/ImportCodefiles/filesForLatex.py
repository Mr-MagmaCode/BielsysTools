# The newest version of the code is available at: https://github.com/Mr-MagmaCode/BielsysTools.git

import argparse
import os
from typing import List, Sequence, Optional, Dict, Tuple


def find_source_files(
    root_dir: str,
    exts: Sequence[str] = (".c", ".cpp", ".h", ".hpp", ".py"),
    exclude_prefixes: Sequence[str] = ("_", ".", "cmake"),
    exclude_files: Optional[Sequence[str]] = None,
) -> List[str]:
    if exclude_files is None:
        exclude_files = []
    file_list: List[str] = []
    # ensure we pass a tuple[str, ...] to str.endswith for correct typing
    exts_tuple = tuple(exts)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directories starting with _ or .
        dirnames[:] = [d for d in dirnames if not (d.startswith("_") or d.startswith("."))]
        for filename in filenames:
            # Exclude files starting with _ or . or cmake folder, and excluded files
            if (
                filename.endswith(exts_tuple)
                and not any(filename.startswith(prefix) for prefix in exclude_prefixes)
                and filename not in exclude_files
            ):
                rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                file_list.append(rel_path)
    return sort_source_files(file_list)


def sort_source_files(file_list: Sequence[str]) -> List[str]:
    """Sort files so that `main.h` and `main.c` appear first (header before c),
    and for other matching pairs the `.h` appears before the corresponding `.c`.
    Sorting keeps files grouped by directory and base name.
    """
    def ext_rank(ext: str) -> int:
        e = ext.lower()
        if e in (".h", ".hpp"):
            return 0
        if e in (".c", ".cpp", ".cc", ".cxx"):
            return 1
        return 2

    def keyfunc(rel: str) -> Tuple[int, str, str, int, str]:
        dirpath, filename = os.path.split(rel)
        base, ext = os.path.splitext(filename)
        base_lower = base.lower()
        is_main = (base_lower == "main")
        # Priority: main headers (0), main sources (1), others (2)
        if is_main:
            if ext.lower() in (".h", ".hpp"):
                pri = 0
            elif ext.lower() in (".c", ".cpp", ".cc", ".cxx"):
                pri = 1
            else:
                pri = 2
        else:
            pri = 2
        # Ensure mains are at absolute top by using empty dirkey for them
        dirkey = "" if is_main else dirpath.lower()
        return (pri, dirkey, base_lower, ext_rank(ext), rel.lower())

    return sorted(list(file_list), key=keyfunc)


def generate_latex_for_files(
    file_list: Sequence[str],
    section_title: Optional[str] = None,
    folder_in_latex: str = "Kode",
    language_override: Optional[str] = None,
    ext_lang_map: Optional[Dict[str, str]] = None,
) -> str:
    """Generate LaTeX code for the given file list."""
    latex_content: List[str] = []
    # Default section title when None supplied
    if section_title is None:
        section_title = "Kode vedlegg"

    if section_title != "":
        latex_content.append(f"\\section{{{section_title}}}")
        latex_content.append("")

    def get_minted_language(filename: str, ext_lang_map: Optional[Dict[str, str]] = None) -> str:
        """Return a sensible minted/Pygments language for a filename based on extension.

        Defaults to 'text' if extension is unknown.
        """
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        # allow caller-provided per-extension overrides (keys like '.h' -> 'cpp')
        if ext_lang_map:
            # ensure lookup uses lowercased ext with leading dot
            key = ext if ext.startswith(".") else f".{ext}"
            if key in ext_lang_map:
                return ext_lang_map[key]
        mapping: Dict[str, str] = {
            ".py": "python",
            ".c": "c",
            ".h": "c",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".hpp": "cpp",
        }
        return mapping.get(ext, "text")

    for i, f in enumerate(file_list):
        if not (section_title != "" and i == 0):
            latex_content.append("\\newpage")
        latex_content.append(f"\\label{{sec:{f.replace('.', '_').replace('/', '_')}}}")
        latex_content.append(f"\\subsection{{{f.replace('_', '\\_')}}}")
        # If a global override is provided, use it verbatim. Otherwise detect by extension.
        lang = language_override if language_override else get_minted_language(f, ext_lang_map)
        latex_content.append(f"\\inputminted{{{lang}}}{{{folder_in_latex}/{f}}}")
    return "\n".join(latex_content)


def print_latex_for_files(
    file_list: Sequence[str],
    section_title: Optional[str] = None,
    folder_in_latex: str = "Kode",
    language_override: Optional[str] = None,
    ext_lang_map: Optional[Dict[str, str]] = None,
) -> None:
    """Print LaTeX code to console."""
    latex_content = generate_latex_for_files(
        file_list, section_title=section_title, folder_in_latex=folder_in_latex, language_override=language_override, ext_lang_map=ext_lang_map
    )
    print(latex_content)


def save_latex_to_file(
    file_list: Sequence[str],
    output_file: str,
    section_title: Optional[str] = None,
    folder_in_latex: str = "Kode",
    language_override: Optional[str] = None,
    ext_lang_map: Optional[Dict[str, str]] = None,
) -> bool:
    """Save LaTeX code to a .tex file."""
    latex_content = generate_latex_for_files(
        file_list, section_title=section_title, folder_in_latex=folder_in_latex, language_override=language_override, ext_lang_map=ext_lang_map
    )

    # Ensure the output file has .tex extension
    if not output_file.endswith(".tex"):
        output_file += ".tex"

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(latex_content)
        print(f"LaTeX code saved to: {output_file}")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False


def generate_CLI_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate LaTeX code for source files")
    parser.add_argument("-o", "--output", type=str, help="Output .tex file (if not specified, prints to console)")
    parser.add_argument("--folder", type=str, default="Kode", help="Folder name to use in LaTeX (default: Kode)")
    parser.add_argument("--section", type=str, default="", help="Section title in LaTeX (if empty, no section will be added)")
    parser.add_argument("--language-override", type=str, default=None, help="Force minted language for all files (overrides detection). Example: 'C++' or 'cpp' or 'python'.")
    parser.add_argument("--lang-map", type=str, default=None, help="Comma-separated per-extension mapping, e.g. '.h=cpp,.py=python'. Keys may omit the leading dot.")
    parser.add_argument("--include-self", action="store_true", help="Include this script in the generated file list (default: excluded)")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = generate_CLI_args()

    root = os.path.dirname(os.path.abspath(__file__))
    this_file = os.path.basename(__file__)
    # By default exclude this script from the generated file list; allow
    # overriding with `--include-self`.
    exclude_files_arg = None if args.include_self else [this_file]
    files = find_source_files(root, exclude_files=exclude_files_arg)

    # Parse per-extension mapping string into a dict like {'.h':'cpp', '.py':'python'}
    ext_lang_map: Optional[Dict[str, str]] = None
    if args.lang_map:
        ext_lang_map = {}
        for pair in args.lang_map.split(","):
            if not pair:
                continue
            if "=" not in pair:
                continue
            key, val = pair.split("=", 1)
            key = key.strip().lower()
            val = val.strip()
            if not key.startswith("."):
                key = "." + key
            ext_lang_map[key] = val

    if args.output:
        save_latex_to_file(
            file_list=files,
            output_file=args.output,
            section_title=args.section,
            folder_in_latex=args.folder,
            language_override=args.language_override,
            ext_lang_map=ext_lang_map,
        )
    else:
        print_latex_for_files(
            file_list=files,
            section_title=args.section,
            folder_in_latex=args.folder,
            language_override=args.language_override,
            ext_lang_map=ext_lang_map,
        )
