# FileStructure-To-Text

## Overview

`FileStructure-To-Text` is a simple Python program that generates a text-based representation of a directory's structure. It takes a folder as input and recursively traverses its subdirectories, printing out the structure in a clear, tree-like format.

## Features

- Recursively traverses directories and subdirectories.
- Differentiates between files and directories in the output.
- Provides a clean and organized visual representation of a folder's structure.

## Example Output

When you run the program on a folder, the output will look something like this:

![Demo](Demo.png)

```python


# Absolute File Path: /Users/mac/Desktop/204/SearchAndSort


./SearchAndSort/*
        ├─ bin/*
        |       ├─ algorithms/*
        |       |       └─ .DS_Store
        |       └─ .DS_Store
        ├─ lib/*
        ├─ .vscode/*
        |       └─ settings.json
        ├─ src/*
        |       ├─ algorithms/*
        |       |       ├─ .DS_Store
        |       |       ├─ SearchAlgorithms.java
        |       |       └─ SortAlgorithms.java
        |       ├─ .DS_Store
        |       └─ App.java
        ├─ 204 GROUP WORK A3.pdf
        ├─ .DS_Store
        └─ README.md


```


## How to Use

1. **Clone the Repository:**
   - Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/Programming-Sai/FileStructure-To-Text.git
   ```

2. **Navigate to the Folder:**

- Change into the directory where the script is located:
    ```bash
    cd FileStructure-To-Text
    ```

3. **Run the Script:**
- Execute the Python script by running:
    ```bash
    python main.py

        OR

    python3 main.py # If on a mac
    ```

4. **Input Folder Path:**
- When prompted, enter the absolute path of the folder whose structure you want to visualize.


## Requirements
Python 3.x
