import fnmatch
import os
import subprocess
import platform
import argparse

def install():
    """
    Install the FTT command by copying the main Python script to a standard location
    and creating an executable script for running the command.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == "Windows":
        # Execute the Windows setup script
        bat_file = os.path.join(script_dir, "setup.bat")
        subprocess.call(['powershell', '-Command', f'Start-Process "{bat_file}" -Verb RunAs'])    
    else:
        # Execute the Unix-like setup script
        subprocess.call(["bash", os.path.join(script_dir, "setup.sh")])

def uninstall():
    """
    Uninstall the FTT command by removing the installed files and cleaning up.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == "Windows":
        # Execute the Windows uninstall script
        subprocess.call([os.path.join(script_dir, "uninstall.bat")], shell=True)
    else:
        # Execute the Unix-like uninstall script
        subprocess.call(["bash", os.path.join(script_dir, "uninstall.sh")])

def visualize(folder):
    """
    Visualize the directory structure of the specified folder.

    Parameters:
    folder (str): The path to the folder to be visualized.

    If the folder does not exist, an error message is printed.
    """
    if not os.path.isdir(folder):
        print(f"Sorry, folder '{folder}' not found.")
        return

    try:
        file_to_text(folder)
    except FileNotFoundError:
        print(f"\nSorry Folder '{folder}' not found. If it truly exists then navigate to it and run the command `ftt` again, or stay where you are and run the command `ftt <path/to/{folder}`\n")
    except Exception as e:
        print(f"\nSorry an error has occurred. Please Try Again:\nError: \t\n {e}\n")



def file_to_text(folder, depth=0, prefix="", exemptions=[]):
    """
    Recursively traverse a directory and print its structure in a tree-like format.

    Parameters:
    folder (str): The path to the folder to be traversed.
    depth (int): The current depth in the directory tree (used for formatting). Defaults to 0.
    prefix (str): The prefix string used to format the tree structure. Defaults to an empty string.
    exemptions (list): List of paths or filenames to exclude, supports wildcards.

    Returns:
    None
    """
    print("\n\n./" + os.path.basename(folder) + '/*') if depth == 0 else ""

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

        return False

    # Filter directories and files
    dirs = [os.path.join(folder, i) for i in items if os.path.isdir(os.path.join(folder, i)) and not is_exempted(os.path.join(folder, i))]
    files = [os.path.join(folder, i) for i in items if not os.path.isdir(os.path.join(folder, i)) and not is_exempted(os.path.join(folder, i))]

    # Print directories
    for i, d in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1) and not files
        connector = "\t└─" if is_last_dir else "\t├─"
        print(prefix + connector + " " + os.path.basename(d) + '/*')
        new_prefix = prefix + ("    " if is_last_dir else "\t|   ")
        file_to_text(os.path.join(folder, os.path.basename(d)), depth + 1, new_prefix, exemptions)

    # Print files
    for i, f in enumerate(files):
        is_last_file = (i == len(files) - 1)
        connector = "\t└─" if is_last_file else "\t├─"
        print(prefix + connector + " " + os.path.basename(f))

    print("\n\n") if depth == 0 else ""




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
    parser.add_argument('command', type=str, nargs='?', help='Command to execute (install, uninstall, or <folder_name>)')
    args = parser.parse_args()

    if args.command == 'install':
        install()
    elif args.command == 'uninstall':
        uninstall()
    elif args.command is None:
        visualize(os.getcwd())
    else:
        visualize(args.command)

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
        "file 1 - Copy - Copy.txt"  # Exclude this file from the root
    ]
    exemptions4=[]
    exemptions5 = [
        "*.log",
        "*.txt",
        "*/dir 1 - Copy/*",
    ]


    folder = r"C:\Users\pc\Desktop\j"
    # file_to_text(folder)
    file_to_text(folder, exemptions=exemptions1)
    file_to_text(folder, exemptions=exemptions2)
    file_to_text(folder, exemptions=exemptions3)
    file_to_text(folder, exemptions=exemptions4)
    file_to_text(folder, exemptions=exemptions5)

