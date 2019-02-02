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


# Converts the files to wav than sorts them than splices them into 10 sec clips
os.system("python3 createSpectrogram.py " + sys.argv[1] + " true")

# Goes through the list of folders and runs the main script one folder at a time
# So that it does not hog memory because there is some kind of memory error
dirlist = list_dirs(sys.argv[1])
for dir in dirlist:
    os.system("python3 createSpectrogram.py " + dir + " false ")
