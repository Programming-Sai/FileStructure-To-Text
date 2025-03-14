# FileStructure-To-Text

## Overview

**FileStructure-To-Text (FTT)** is a simple Python tool that generates a text-based representation of a directory's structure or creates a folder structure based on a provided template. The tool supports customizable output options (e.g., excluding hidden files, limiting depth, or displaying only files or directories).

> **Warning:**
>
> - This is an MVP version. The tool is provided "as-is" and may have bugs.
> - **Important:** You must supply absolute paths when using FTT to visualize directories.
> - FTT no longer includes dedicated install or uninstall scripts. Instead, you run the tool directly via the command line.
> - After building a standalone executable (using PyInstaller), ensure that its containing folder is added to your system `PATH`. If it isn't, you may need to add it manually.
> - When generating a folder structure from a template, **do not include empty folders** in your template. If an empty folder is required, add a placeholder file (e.g., `.fttkeep`) inside it.
> - If the generated structure is missing some files, try running the generation process two more times. If files are still missing, then there may be an issue with the predefined template.

## Features

- **Directory Visualization:**  
  Recursively traverse directories and display a clean, tree-like structure of files and subdirectories.
- **Structure Generation:**  
  Generate a folder (and file) structure from a user-defined template. The template can be provided as a direct string or as a path to a text file.

- **Customizable Output:**
  - **Exclusions:** Specify files or folders to exclude via wildcard patterns or by providing a file with exclusions (e.g., a `.fttignore` file).
  - **Hidden Files:** Optionally include hidden files and directories.
  - **Depth Limiting:** Limit the recursion depth for visualization.
  - **Output Filters:** Choose to display only directories or only files.
- **Command-Line Interface:**  
  Uses `argparse` to support various optional arguments for flexible usage.

## Example Output

When you run FTT on a folder, the output might look like this:

```graphql

./SearchAndSort/*
        ├─ bin/*
        |       ├─ algorithms/*
        |       |       └─ ... (files)
        |       └─ ... (other files)
        ├─ lib/*
        ├─ .vscode/*
        |       └─ settings.json
        ├─ src/*
        |       ├─ algorithms/*
        |       |       ├─ SearchAlgorithms.java
        |       |       └─ SortAlgorithms.java
        |       └─ App.java
        ├─ 204 GROUP WORK A3.pdf
        └─ README.md

```

When generating a folder structure from a template, you might define a template like this:

```graphql

Project/*
    ├─ src/*
    │   ├─ main.py
    │   └─ utils.py
    ├─ docs/*
    │   └─ README.md
    ├─ config.json
    └─ .gitignore

```

The tool will then create the corresponding folders and files in the specified target directory.

## How to Use

### 1. Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/Programming-Sai/FileStructure-To-Text.git
```

### 2. Navigate to the Project Directory

Change into the directory where the script is located:

```bash
cd FileStructure-To-Text
```

### 3. Running FTT for Visualization

To visualize a folder's structure, run:

```bash
python main.py -f "C:\Absolute\Path\To\Folder"
```

_Note: The folder path must be absolute._

### 4. Running FTT for Structure Generation

To generate a folder structure from a template, you can provide the template either as a direct string or as a file:

```psh
python main.py "
>> Project/*
>>     ├─ src/*
>>     │   ├─ main.py
>>     │   └─ utils.py
>>     ├─ docs/*
>>     │   └─ README.md
>>     ├─ config.json
>>     └─ .gitignore
>> " -f "C:\Users\pc\Desktop\j"
```

Or if your template is saved in a file (e.g., `template.txt`):

```bash
python main.py template.txt -f "C:\Absolute\Path\To\TargetFolder"
```

### 5. Additional Options

- **Exemptions:**  
  To exclude specific files or folders, pass them using the `-e` or `--exemptions` flag:
  ```bash
  python main.py -f "C:\Folder" -e "*.log" "node_modules" ".fttignore"
  ```
- **Hidden Files:**  
  Exclude hidden files (files starting with a dot) using the `-H` flag:
  ```bash
  python main.py -f "C:\Folder" -H
  ```
- **Filter Output:**  
  Show only directories with `-d` or only files with `-F`:
  ```bash
  python main.py -f "C:\Folder" -d
  python main.py -f "C:\Folder" -F
  ```
- **Limit Traversal Depth:**  
  Use the `-m` flag to limit directory traversal depth:

  ```bash
  python main.py -f "C:\Folder" -m 3
  ```

- **Save Output to File:**  
  Save the visualization output to a file using the `-s` flag:

  ```bash
  python main.py -f "C:\Folder" -s output.txt
  ```

- **Version Information:**  
  View version information with the `-v` flag:
  ```bash
  python main.py -v
  ```

## Installation

To install FTT as a standalone, globally available executable:

1. **Build the Executable:**  
   Run the build script:

   ```bash
   python build.py
   ```

   This script will:

   - Build a standalone executable using PyInstaller.
   - Copy the executable to the appropriate installation directory.
   - Attempt to add that directory to your system `PATH`.

2. **Post-Installation:**

   - **Important:** If the executable is not recognized after installation, restart your terminal (or VS Code) and try again.
   - If the executable is still not recognized, manually add the installation directory (e.g., `C:\Users\pc\AppData\Local\Programs\FTT`) to your system `PATH` OR use this to help you [troubleshoot](https://chatgpt.com/).

3. **Usage of Installed Executable:**  
   Once installed, you can run FTT globally by simply typing:

   ```bash
   ftt
   ```

   in your terminal.

   **Example:**

   ```bash
   ftt -f "C:\Absolute\Path\To\Folder"
   ```

   **Additional Options**

- **Exemptions:**  
  To exclude specific files or folders, pass them using the `-e` or `--exemptions` flag:
  ```bash
  ftt -f "C:\Folder" -e "*.log" "node_modules" ".fttignore"
  ```
- **Hidden Files:**  
  Exclude hidden files (files starting with a dot) using the `-H` flag:
  ```bash
  ftt -f "C:\Folder" -H
  ```
- **Filter Output:**  
  Show only directories with `-d` or only files with `-F`:
  ```bash
  ftt -f "C:\Folder" -d
  ftt -f "C:\Folder" -F
  ```
- **Limit Traversal Depth:**  
  Use the `-m` flag to limit directory traversal depth:

  ```bash
  ftt -f "C:\Folder" -m 3
  ```

- **Save Output to File:**  
  Save the visualization output to a file using the `-s` flag:

  ```bash
  ftt -f "C:\Folder" -s output.txt
  ```

- **Version Information:**  
  View version information with the `-v` flag:
  ```bash
  ftt -v
  ```

## Requirements

- Python 3.x

## Warnings & Important Notes

- **Absolute Paths Required:**  
  When visualizing, always provide an absolute path for the folder. Relative paths are not supported.
- **No Install/Uninstall Scripts:**  
  This version does not include dedicated install or uninstall scripts. You run the tool directly via the command line.
- **PATH Configuration:**  
  After building a standalone executable (using PyInstaller), ensure that its containing folder is added to your system `PATH` if you want to run it globally.
- **Environment:**  
  The tool is in MVP stage. Future releases may include additional features, improvements, and bug fixes. Always check for updates.
- **Error Handling:**  
  If you encounter any errors during use, please file an issue on GitHub with details and steps to reproduce the problem.
- **Empty Folders:**  
  No Empty folders must be included in your folder structure when trying to generate files. so something like this:

  ```graphql

    Project/*
        ├─ empty/*
        ├─ src/*
        │   ├─ main.py
        │   └─ utils.py
        ├─ docs/*
        │   └─ README.md
        ├─ config.json
        └─ .gitignore

  ```

  would not be a good idea to do. This would be better:

  ```graphql

  Project/*
      ├─ empty/*
      │   └─ .fttkeep
      ├─ src/*
      │   ├─ main.py
      │   └─ utils.py
      ├─ docs/*
      │   └─ README.md
      ├─ config.json
      └─ .gitignore

  ```

---
