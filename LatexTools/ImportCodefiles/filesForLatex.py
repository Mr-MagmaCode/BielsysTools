import os
import argparse


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


def generate_latex_for_files(file_list, section_title="Kode vedlegg", folder_in_latex="Kode"):
    """Generate LaTeX code for the given file list."""
    latex_content = []
    if section_title != "" and section_title is not None:
        latex_content.append(f"\\section{{{section_title}}}")
        latex_content.append("")
    for f in file_list:
        latex_content.append(f"\\newpage")
        latex_content.append(
            f"\\label{{sec:{f.replace('.', '_').replace('/', '_')}}}")
        latex_content.append(f"\\subsection{{{f.replace('_', '\\_')}}}")
        latex_content.append(
            f"\\inputminted{{C++}}{{{folder_in_latex}/{f}}}\n")
    return "\n".join(latex_content)


def print_latex_for_files(file_list, section_title=None, folder_in_latex="Kode"):
    """Print LaTeX code to console."""
    latex_content = generate_latex_for_files(
        file_list, section_title=section_title, folder_in_latex=folder_in_latex)
    print(latex_content)


def save_latex_to_file(file_list, output_file, section_title=None, folder_in_latex="Kode"):
    """Save LaTeX code to a .tex file."""
    latex_content = generate_latex_for_files(
        file_list, section_title=section_title, folder_in_latex=folder_in_latex)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate LaTeX code for source files")
    parser.add_argument("-o", "--output", type=str,
                        help="Output .tex file (if not specified, prints to console)")
    parser.add_argument("--folder", type=str, default="Kode",
                        help="Folder name to use in LaTeX (default: Kode)")
    parser.add_argument("--section", type=str, default="",
                        help="Section title in LaTeX (if empty, no section will be added)")

    args = parser.parse_args()

    root = os.path.dirname(os.path.abspath(__file__))
    this_file = os.path.basename(__file__)
    files = find_source_files(root)

    if args.output:
        save_latex_to_file(file_list=files, output_file=args.output,
                           section_title=args.section, folder_in_latex=args.folder)
    else:
        print_latex_for_files(
            file_list=files, section_title=args.section, folder_in_latex=args.folder)
