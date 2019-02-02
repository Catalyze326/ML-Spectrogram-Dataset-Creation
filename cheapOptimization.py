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


# List files in a directory going recursively.
def list_files(loc):
    filelist = []
    dirlist = list_dirs(loc)
    for path, dirs, files in os.walk(loc):
        for f in files:
            filelist.append(path + "/" + f)
    for dir in dirlist:
        for path, dirs, files in os.walk(dir):
            for f in files:
                filelist.append(path + "/" + f)
    for file in filelist:
        print("We found " + file)

    return filelist


def log(toWrite):
    log.write(toWrite)


# Puts folders into groups of 25 at a time
def sort_into_groups(size):
    filelist = list_files(sys.argv[1])
    i = 0
    j = 0
    while i < len(filelist) - 1:
        folder, lol = os.path.split(filelist[0])
        try:
            os.mkdir(folder + "/" + "folder#" + str(j))
        except:
            print("The folder " + folder + "/" + "folder#" + str(j) + "already exists")
            # log.write("The folder " + folder + "/" + "folder#" + str(j) + "already exists")
        j += 1
        for k in range(size):
            if len(filelist) <= i:
                break
            folder, lol = os.path.split(filelist[i])
            try:
                os.rename(filelist[i], folder + "/" + "folder#" + str(j - 1) + "/" + lol)
            except:
                print("It has already been sorted")
            i += 1
            k += 1


# log = open("log " + time.asctime() + ".txt", "w")
sort_into_groups(25)
dirlist = list_dirs(sys.argv[1])
for dir in dirlist:
    os.system("python3 createSpectrogram.py " + dir)
