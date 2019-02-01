import os
import sys

# returns a list of the directories in a folder
def list_dirs(loc):
    dirlist = []
    for path, dirs, files in os.walk(loc):
        for d in dirs:
            lol = (path + "/" + d)
            dirlist.append(lol)
    return dirlist


dirlist = list_dirs(sys.argv[1])
for dir in dirlist:
	os.system("python3 main.py " + dir)
