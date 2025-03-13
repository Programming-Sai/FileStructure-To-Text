import os
import re


s = '''
./j/*
        ├─ dir 1/*
        |       ├─ a - Copy (2).log
        |       ├─ d - Copy (2).json
        |       ├─ d.sh
        |       ├─ file 1 - Copy (2).txt
        |       ├─ file 1 - Copy (3).txt
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
        ├─ a.log
        ├─ d - Copy (3) - Copy.json
        ├─ d - Copy.sh
        ├─ file 1 - Copy - Copy.txt
        ├─ file 1 - Copy.txt
        └─ file 1.txt

'''


def parser(structure, root, result=[], folders=[]):
    lines = structure.strip().split("\n")    
    for i, line in enumerate(lines):

        line=re.sub(r"\s+", "", line)
        
        if line.endswith("/*"):
            folders.append(line.replace("/*", '').replace("./", '').replace("├─", '').replace("|", '').replace("\t", ''))
        elif "└─" in line:
            result.append(os.path.join(root, *folders[1:], line.replace("/*", '').replace("/", '').replace("├─", '').replace("|", '').replace("\t", '').replace("└─", '')))
            folders.pop()
        else:
            result.append(os.path.join(root, *folders[1:], line.replace("/*", '').replace("/", '').replace("├─", '').replace("|", '').replace("\t", '').replace("└─", '')))
    return result


# Example usage
root = r"C:\Users\pc\Desktop\j"
file_paths = parser(s, root)
# file_paths = parse_structure(s, root)

# print(os.path.join(root, *['r', 'g', 'h'], "Hello.txt"))
print(len(file_paths))
for path in file_paths:
    print(path), 
