import os
import re


s = '''
./j/*
        ├─ dir 1/*
        |       ├─ a - Copy (2).log
        |       ├─ d -1 - Copy (3).txt
        |       └─ file 1 - Copy (4).txt
        ├─ dir 2/*
        |       ├─ dir 1 - Copy/*
        |       |       ├─ file 1 - Copy (2).txt
        |       |       ├─ file 1 - Copy (3).txt
        |       |       └─ file 1 - Copy (4).txt
        |       ├─ file 1 - Copy - Copy (2).txt
        |       ├─ file 1 - Copy - Copy (3).txt
        |       └─ file 1 - Copy - Copy (4).txt
        ├─ a - Copy (3).log
        ├─ a - Copy.log
        ├─ a.log Copy (2).json
        |       ├─ d.sh
        |       ├─ file 1 - Copy (2).txt
        |       ├─ file 
        ├─ d - Copy (3) - Copy.json
        ├─ d - Copy.sh
        ├─ file 1 - Copy - Copy.txt
        ├─ file 1 - Copy.txt
        └─ file 1.txt
'''


def parse_structure(structure, root_folder, prefix=""):
    """
    Parses a directory tree structure string and extracts absolute file paths.

    Parameters:
    structure (str): The formatted directory structure as a string.
    root_folder (str): The root directory path.

    Returns:
    list: A list of absolute file paths.
    """
    lines = structure.strip().split("\n")
    file_paths = []
    dir_stack = [prefix if prefix else root_folder]  # Track directory depth

    for i, line in enumerate(lines):
        match = re.match(r"(\s*)(├─|└─)\s(.+)", line)
        if not match:
            continue

        indent, _, name = match.groups()
        level = indent.count("│")  # Determine depth based on vertical bars

        while len(dir_stack) > level + 1:
            dir_stack.pop()  # Adjust stack if indentation decreases

        current_path = os.path.join(dir_stack[-1], name.replace("/*", ""))

        if name.endswith("/*"):  # Directory
            dir_stack.append(current_path)
        else:  # File
            file_paths.append(current_path)

    return file_paths




# Example usage
root = r"C:\Users\pc\Desktop\j"
file_paths = parse_structure(s, root)

for path in file_paths:
    print(path)
