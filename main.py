import os


def file_to_text(folder, depth=0, prefix=""):

    """
        Recursively traverses a directory and prints its structure in a tree-like format.

        Parameters:
        folder (str): The path to the folder to be traversed.
        depth (int): The current depth in the directory tree (used for formatting). Defaults to 0.
        prefix (str): The prefix string used to format the tree structure. Defaults to an empty string.

        Returns:
        None
    """


    # Print the base directory if at the root level
    print("\n\n./" + os.path.basename(folder) + '/*') if depth == 0 else ""

    # Get list of all items in the folder
    items = os.listdir(folder)
    dirs = [i for i in items if os.path.isdir(os.path.join(folder, i))]
    files = [i for i in items if not os.path.isdir(os.path.join(folder, i))]

    # Process directories
    for i, d in enumerate(dirs):
        # Determine if this is the last directory in the list and if there are no files
        is_last_dir = (i == len(dirs) - 1) and not files
        # Set the appropriate connector symbol
        connector = "\t└─" if is_last_dir else "\t├─"
        # Print the directory with the appropriate prefix
        print(prefix + connector + " " + d + '/*')
        # Update the prefix for nested items
        new_prefix = prefix + ("    " if is_last_dir else "\t|   ")
        # Recursively call the function for the subdirectory
        file_to_text(os.path.join(folder, d), depth + 1, new_prefix)
    
    # Process files
    for i, f in enumerate(files):
        # Determine if this is the last file in the list
        is_last_file = (i == len(files) - 1)
        # Set the appropriate connector symbol
        connector = "\t└─" if is_last_file else "\t├─"
        # Print the file with the appropriate prefix
        print(prefix + connector + " " + f)

    # Add a newline after printing the root directory structure
    print("\n\n") if depth == 0 else ""







# Start the process by taking a folder path as input from the user
file_to_text(input("\n\nEnter File Path: "))




