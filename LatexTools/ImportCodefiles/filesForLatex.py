import argparse
import os


def find_source_files(root_dir, exts=(".c", ".cpp", ".h", ".hpp", ".py"), exclude_prefixes=("_", ".", "cmake"), exclude_files=None):
    if exclude_files is None:
        exclude_files = []
    file_list = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directories starting with _ or .
        dirnames[:] = [d for d in dirnames if not (
            d.startswith("_") or d.startswith("."))]
        for filename in filenames:
            # Exclude files starting with _ or . or cmake folder, and excluded files
            if (filename.endswith(exts)
                    and not any(filename.startswith(prefix) for prefix in exclude_prefixes)
                    and filename not in exclude_files):
                rel_path = os.path.relpath(
                    os.path.join(dirpath, filename), root_dir)
                file_list.append(rel_path)
    return sorted(file_list)


def generate_latex_for_files(file_list, section_title="Kode vedlegg", folder_in_latex="Kode", language_override=None, ext_lang_map=None):
    """Generate LaTeX code for the given file list."""
    latex_content = []
    if section_title != "" and section_title is not None:
        latex_content.append(f"\\section{{{section_title}}}")
        latex_content.append("")

    def get_minted_language(filename, ext_lang_map=None):
        """Return a sensible minted/Pygments language for a filename based on extension.

        Defaults to 'text' if extension is unknown.
        """
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        # allow caller-provided per-extension overrides (keys like '.h' -> 'cpp')
        if ext_lang_map:
            # ensure lookup uses lowercased ext with leading dot
            key = ext if ext.startswith('.') else f'.{ext}'
            if key in ext_lang_map:
                return ext_lang_map[key]
        mapping = {
            '.py': 'python',
            '.c': 'c',
            '.h': 'c',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.hpp': 'cpp',
        }
        return mapping.get(ext, 'text')
    for f in file_list:
        latex_content.append(f"\\newpage")
        latex_content.append(
            f"\\label{{sec:{f.replace('.', '_').replace('/', '_')}}}")
        latex_content.append(f"\\subsection{{{f.replace('_', '\\_')}}}")
        # If a global override is provided, use it verbatim. Otherwise detect by extension.
        lang = language_override if language_override else get_minted_language(
            f, ext_lang_map)
        latex_content.append(
            f"\\inputminted{{{lang}}}{{{folder_in_latex}/{f}}}\\n")
    return "\n".join(latex_content)


def print_latex_for_files(file_list, section_title=None, folder_in_latex="Kode", language_override=None, ext_lang_map=None):
    """Print LaTeX code to console."""
    latex_content = generate_latex_for_files(
        file_list, section_title=section_title, folder_in_latex=folder_in_latex, language_override=language_override, ext_lang_map=ext_lang_map)
    print(latex_content)


def save_latex_to_file(file_list, output_file, section_title=None, folder_in_latex="Kode", language_override=None, ext_lang_map=None):
    """Save LaTeX code to a .tex file."""
    latex_content = generate_latex_for_files(
        file_list, section_title=section_title, folder_in_latex=folder_in_latex, language_override=language_override, ext_lang_map=ext_lang_map)

    # Ensure the output file has .tex extension
    if not output_file.endswith(".tex"):
        output_file += ".tex"

    try:
        with open(output_file, 'w', encoding="utf-8") as f:
            f.write(latex_content)
        print(f"LaTeX code saved to: {output_file}")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False


def generate_CLI_args():
    parser = argparse.ArgumentParser(
        description="Generate LaTeX code for source files")
    parser.add_argument("-o", "--output", type=str,
                        help="Output .tex file (if not specified, prints to console)")
    parser.add_argument("--folder", type=str, default="Kode",
                        help="Folder name to use in LaTeX (default: Kode)")
    parser.add_argument("--section", type=str, default="",
                        help="Section title in LaTeX (if empty, no section will be added)")
    parser.add_argument("--language-override", type=str, default=None,
                        help="Force minted language for all files (overrides detection). Example: 'C++' or 'cpp' or 'python'.")
    parser.add_argument("--lang-map", type=str, default=None,
                        help="Comma-separated per-extension mapping, e.g. '.h=cpp,.py=python'. Keys may omit the leading dot.")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = generate_CLI_args()

    root = os.path.dirname(os.path.abspath(__file__))
    this_file = os.path.basename(__file__)
    files = find_source_files(root)

    # Parse per-extension mapping string into a dict like {'.h':'cpp', '.py':'python'}
    ext_lang_map = None
    if args.lang_map:
        ext_lang_map = {}
        for pair in args.lang_map.split(','):
            if not pair:
                continue
            if '=' not in pair:
                continue
            key, val = pair.split('=', 1)
            key = key.strip().lower()
            val = val.strip()
            if not key.startswith('.'):
                key = '.' + key
            ext_lang_map[key] = val

    if args.output:
        save_latex_to_file(file_list=files, output_file=args.output,
                           section_title=args.section, folder_in_latex=args.folder, language_override=args.language_override, ext_lang_map=ext_lang_map)
    else:
        print_latex_for_files(
            file_list=files, section_title=args.section, folder_in_latex=args.folder, language_override=args.language_override, ext_lang_map=ext_lang_map)
