import fnmatch
import os
import re
import subprocess
import platform
import argparse
import sys
from version import version



def file_to_text_validator(folder):
    """
    Validate and visualize the directory structure of the specified folder.

    Parameters:
    folder (str): The absolute path to the folder to be visualized.

    Returns:
    bool: True if the folder is valid and processed, False otherwise.
    """
    if folder == '.':
        return True
    
    if not os.path.isabs(folder):
        print("Error: Please enter a valid absolute path.")
        sys.exit(1)
    
    if not os.path.isdir(folder):
        print(f"Error: Folder '{folder}' not found.")
        sys.exit(1)

    try:    
        pass
        return True
    except FileNotFoundError:
        print(f"\nError: Folder '{folder}' not found. If it exists, try:\n"
              f"- Navigating to it and running `ftt`\n"
              f"- Running `ftt {folder}` from your current location\n")
    except Exception as e:
        print(f"\nAn unexpected error occurred:\n{e}\n")

    sys.exit(1)


def exemptions_validator(exemptions):
    result = exemptions if exemptions else []
    
    if os.path.exists(os.path.join(os.getcwd(), '.fttignore')):
        result.extend(reading_fttignore())

    return result    


def template_validator(template):
    if os.path.isfile(template):
        try:
            with open(template, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except Exception as e:
            print(f"Error Reading template file: {e}")
            sys.exit(1)
    else:
        template_content = template
    return template_content



def file_to_text(folder, depth=0, prefix="", exemptions=[], exclude_hidden=False, max_depth=None, dirs_only=False, files_only=False, output=None):
    """
        Recursively traverse a directory and print its structure in a tree-like format.

        Parameters:
        folder (str): The path to the folder to be traversed.
        depth (int): The current depth in the directory tree (used for formatting). Defaults to 0.
        prefix (str): The prefix string used to format the tree structure. Defaults to an empty string.
        exemptions (list): List of paths or filenames to exclude, supports wildcards.
        exclude_hidden (bool): Whether to exclude hidden files and folders.
        max_depth (int): Maximum recursion depth.
        dirs_only (bool): If True, only directories will be displayed.
        files_only (bool): If True, only files will be displayed.

        Returns:
        None
    """
    if output is None:
        output = []
    if max_depth is not None and depth >= max_depth: return
    print("\n\n./" + os.path.basename(folder) + '/*') if depth == 0 else ""
    output.append("\n\n./" + os.path.basename(folder) + '/*'+'\n') if depth == 0 else ""

    items = os.listdir(folder)

    # Convert absolute paths for direct matching
    exemptions_abs = {os.path.abspath(j) for j in exemptions}
    exemptions_names = {os.path.basename(j) for j in exemptions}

    def is_exempted(path):
        abs_path = os.path.abspath(path)
        base_name = os.path.basename(path)

        # Check direct absolute and name matches
        if abs_path in exemptions_abs or base_name in exemptions_names:
            return True

        # Check wildcard patterns using fnmatch
        for pattern in exemptions:
            if fnmatch.fnmatch(base_name, pattern) or fnmatch.fnmatch(abs_path, pattern):
                return True
        
        if os.path.basename(path).startswith("."): return exclude_hidden

        return False

    # Filter directories and files
    dirs = [os.path.join(folder, i) for i in items if os.path.isdir(os.path.join(folder, i)) and not is_exempted(os.path.join(folder, i))]
    files = [os.path.join(folder, i) for i in items if not os.path.isdir(os.path.join(folder, i)) and not is_exempted(os.path.join(folder, i))]
    

    if not files_only:
        # Print directories
        for i, d in enumerate(dirs):
            # is_last_dir = (i == len(dirs) - 1) and not files
            is_last_dir = (i == len(dirs) - 1) and (files_only or not files)  # Consider files_only flag
            connector = "\t└─" if is_last_dir else "\t├─"
            print(prefix + connector + " " + os.path.basename(d) + '/*')
            output.append(prefix + connector + " " + os.path.basename(d) + '/*'+'\n')
            new_prefix = prefix + ("    " if is_last_dir else "\t|   ")
            file_to_text(os.path.join(folder, os.path.basename(d)), depth + 1, new_prefix, exemptions, exclude_hidden, max_depth, dirs_only, files_only, output)

    if not dirs_only:
        # Print files
        for i, f in enumerate(files):
            is_last_file = (i == len(files) - 1)
            connector = "\t└─" if is_last_file else "\t├─"
            print(prefix + connector + " " + os.path.basename(f))
            output.append(prefix + connector + " " + os.path.basename(f)+'\n')

    print("\n\n") if depth == 0 else ""
    output.append("\n\n") if depth == 0 else ""
    return output



def structure_parser(structure, root):
    result=[] 
    folders=[]
    lines = structure.strip().split("\n")    
    for i, line in enumerate(lines):

        line=re.sub(r"\s+", "", line)
        
        if line.endswith("/*"):
            folders.append(line.replace("/*", '').replace("./", '').replace("├─", '').replace("|", '').replace("\t", ''))
        elif "└─" in line:
            result.append(os.path.join(root, *folders[(1 if folders and os.path.basename(root) == folders[0] else 0):], line.replace("/*", '').replace("/", '').replace("├─", '').replace("|", '').replace("\t", '').replace("└─", '')))
            folders.pop() if folders else ""
        else:
            result.append(os.path.join(root, *folders[(1 if folders and os.path.basename(root) == folders[0] else 0):], line.replace("/*", '').replace("/", '').replace("├─", '').replace("|", '').replace("\t", '').replace("└─", '')))
    return result



def create_dir(paths):
    for path in paths:
        path=path.replace('|', '')
        
        dir = os.path.dirname(path)

        if dir and not os.path.exists(dir):
            os.makedirs(dir)
            continue

        print("FILE PATH: ", path)
        with open(path, 'w') as f:
            pass


def reading_fttignore():
    exemptions = []
    try:
        with open('.fttignore', 'r') as f:
            exemptions=f.readlines()
    except:
        pass
    return [i.strip() for i in exemptions]


def main():
    """
    Main function to parse command-line arguments and execute the appropriate action.

    Commands:
    - 'install': Runs the install function.
    - 'uninstall': Runs the uninstall function.
    - '<folder_name>': Visualizes the specified folder.
    - (No command): Visualizes the current working directory.
    """


    parser = argparse.ArgumentParser(description='Manage the FTT command.')

    parser.add_argument('-f', '--folder', type=str, default='.', help="Path to the root folder to traverse.")
    parser.add_argument('-e', '--exemptions', type=str, nargs='*', help="List of files/folders to exclude. Accepts either a space-separated list or a file path containing exclusions and adds those to any exemptions spcified in a .fttignore file, if there is any.")
    parser.add_argument('-H', '--hidden', action='store_true', help="Include hidden files and directories in the output. By default, hidden files (starting with '.') are excluded.")

    parser.add_argument('generate', type=str, nargs='?', help="Specify the template for the directory structure. Can be a path to a text file or a direct string.")

    parser.add_argument('-d', '--dirs-only', action='store_true', help="Show only directories in the output.")
    parser.add_argument('-F', '--files-only', action='store_true', help="Show only files in the output.")

    parser.add_argument('-m', '--max-depth', type=int, default=None, help="Limit the depth of directory traversal. Defaults to unlimited.")

    parser.add_argument('-s', '--save-to-file', type=str, nargs='?', const="ftt.txt", help="Save output to a file. Defaults to 'ftt.txt' if no file is provided.")

    parser.add_argument('-v', '--version', action='version', version=f"ftt {version}")



    args = parser.parse_args()
    if args.generate and args.folder and file_to_text_validator(args.folder):
        template=template_validator(args.generate)
        print(template)
        paths=structure_parser(template, args.folder)
        create_dir(paths)
        # for path in paths:
            # print(path)
        print(f"{args.folder} has been created successfully")
    elif args.folder and file_to_text_validator(args.folder):
        output = file_to_text(os.getcwd() if args.folder == '.' else args.folder, exemptions=exemptions_validator(args.exemptions), exclude_hidden=args.hidden if args.hidden else False, max_depth=args.max_depth, dirs_only=args.dirs_only if args.dirs_only else False, files_only=args.files_only if args.files_only else False)
        if args.save_to_file:
            with open('ftt.txt', 'w', encoding='utf-8') as f:
                f.writelines(output) 
            print(f'{args.folder} saved to ftt.txt')
    else:
        file_to_text(os.getcwd())




if __name__ == "__main__":
    exemptions1 = [
        r"C:\Users\pc\Desktop\j\dir 1",  # Exclude entire "dir 1"
        r"C:\Users\pc\Desktop\j\dir 2\dir 1 - Copy\file 1 - Copy (2).txt",  # Exclude specific file
        r"C:\Users\pc\Desktop\j\file 1 - Copy.txt"  # Exclude a single file in root
    ]
    exemptions2 = [
        r"C:\Users\pc\Desktop\j\dir 2",  # Exclude "dir 2" only from the root
        "file 1.txt",  # Exclude "file 1.txt" no matter where it appears
    ]
    exemptions3 = [
        "dir 1",  # Exclude "dir 1" inside "j"
        "dir 2/dir 1 - Copy/file 1 - Copy (2).txt",  # Exclude this exact relative file
        "file 1 - Copy - Copy.txt"  
        "df"
    ]
    exemptions4=[]
    exemptions5 = [
        "*.log",
        "*.txt",
        "*/dir 1 - Copy/*",
    ]
    exemptions6 = reading_fttignore()


    folder = r"c:\Users\pc\Desktop\FileStructure-To-Text"

    main()

    # file_to_text(folder, exemptions=exemptions3, exclude_hidden=True)
    

