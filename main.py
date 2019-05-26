import os
import sys
import threading
import multiprocessing


# returns a list of the directories in a folder
def list_dirs(loc):
    dirlist = []
    for path, dirs, files in os.walk(loc):
        for d in dirs:
            lol = (path + "/" + d)
            dirlist.append(lol)
    return dirlist


def create_spect(dir):
    os.system("python3 createSpectrogram.py " + dir + " false ")


os.system("python3 createSpectrogram.py " + sys.argv[1] + " true")

# TODO put something in to kill it with ctrl + c
i = 0
cores = multiprocessing.cpu_count()
dirlist = list_dirs(sys.argv[1])
length = len(dirlist)
print(length)
while i < length:
    if threading.activeCount() <= cores:
        t1 = threading.Thread(target=create_spect, args=(dirlist[i],))
        i += 1
        t1.start()
        print("There are currently " + str(threading.active_count()) + " threads running")
        print(str(i) + "/" + str(len(dirlist)))
    else:
        t1.join()
