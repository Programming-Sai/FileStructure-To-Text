import os
import re
import sys
import fnmatch
import argparse
from version import version



def file_to_text_validator(folder):
    """
        Validates the given directory path and ensures it exists.

        Parameters:
            folder (str): The absolute path of the folder to validate.

        Returns:
            bool: True if the folder is valid, otherwise exits the program.

        Raises:
            SystemExit: If the folder does not exist or the path is not absolute.
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
    """
        Combines user-specified exemptions with the ones listed in `.fttignore` (if present).

        Parameters:
            exemptions (list[str] | None): A list of files/folders to be excluded.

        Returns:
            list[str]: Updated list of exemptions.
    """
    result = exemptions if exemptions else []
    
    if os.path.exists(os.path.join(os.getcwd(), '.fttignore')):
        result.extend(reading_fttignore())

    return result    


def template_validator(template):
    """
        Validates and reads a template file or uses the provided template string.

        Parameters:
            template (str): A file path or raw string representing the directory structure.

        Returns:
            str: The template content.

        Raises:
            SystemExit: If an error occurs while reading the file.
    """
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
        Recursively generates a textual representation of a directory structure.

        Parameters:
            folder (str): The path to the root directory.
            depth (int): The current depth in the traversal. Default is 0.
            prefix (str): Prefix for formatting tree structure.
            exemptions (list[str]): List of filenames or patterns to exclude.
            exclude_hidden (bool): If True, hidden files and folders are excluded.
            max_depth (int | None): The maximum depth to traverse.
            dirs_only (bool): If True, only directories are displayed.
            files_only (bool): If True, only files are displayed.
            output (list[str] | None): Accumulator for output storage.

        Returns:
            list[str]: A list of formatted strings representing the directory structure.
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

    def is_exempted(path: str) -> bool:
        """Checks if a given path matches exemption patterns."""
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
    """
        Parses a textual directory structure into a list of valid paths.

        Parameters:
            structure (str): The textual representation of the directory.
            root (str): The root directory path.

        Returns:
            list[str]: List of parsed file and directory paths.
    """
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
    """
        Creates directories and files based on a given list of paths.

        Parameters:
            paths (list[str]): A list of paths representing files and folders.

        Returns:
            None
    """
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
    """
        Reads the `.fttignore` file and returns a list of ignored files and folders.

        Returns:
            list[str]: List of ignored paths.
    """
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
        - Providing a folder name with a template: Generates the specified directory structure.
        - Providing only a folder name: Visualizes the folder structure.
        - No folder name (default): Visualizes the current working directory structure.
        - Additional flags allow customization such as filtering files, limiting depth, and saving output.
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
        print(f"{args.folder} has been created successfully")
    elif args.folder and file_to_text_validator(args.folder):
        output = file_to_text(os.getcwd() if args.folder == '.' else args.folder, exemptions=exemptions_validator(args.exemptions), exclude_hidden=args.hidden if args.hidden else False, max_depth=args.max_depth, dirs_only=args.dirs_only if args.dirs_only else False, files_only=args.files_only if args.files_only else False)
        if args.save_to_file:
            with open(args.save_to_file or 'ftt.txt', 'w', encoding='utf-8') as f:
                f.writelines(output) 
            print(f'{args.folder} saved to {args.save_to_file or 'ftt.txt'}')
    else:
        file_to_text(os.getcwd())




if __name__ == "__main__":
    main()
