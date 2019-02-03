import os
import sys
import threading


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


print("python3 createSpectrogram.py " + sys.argv[1] + " true")
os.system("python3 createSpectrogram.py " + sys.argv[1] + " true")

i = 0;
dirlist = list_dirs(sys.argv[1])
for i in range(len(dirlist)):
    if not threading.activeCount() >= 12:
        t1 = threading.Thread(target=create_spect, args=(dirlist[i],))
        i += 1
        t1.start()
        print("There are currently " + str(threading.active_count()) + " threads running")
    else:
        t1.join()
