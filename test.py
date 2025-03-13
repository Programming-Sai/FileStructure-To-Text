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

l = s.split("\n")
# print(l)

