#!/usr/bin/env python
# coding: utf-8
from pydub import AudioSegment
import pydub
import wave
import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
import sys
import os
import os.path
import time
import contextlib
import logging


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


# returns a list of the directories in a folder
def list_dirs(loc):
    dirlist = []
    for path, dirs, files in os.walk(loc):
        for d in dirs:
            lol = (path + "/" + d)
            dirlist.append(lol)
    return dirlist


# This sorts files each into its own directory named after the file
# I ended up not using this method, but I might go back to it at somepoint
# NOTE this must be used before splitting or else you will get a ton of folders
def sort_files():
    filelist = list_files(sys.argv[1])
    for filename in filelist:
        folder, file = os.path.split(filename)
        # Make the folder for each file
        try:
            os.mkdir(filename.split(".")[0])
        except OSError:
            print("The folder " + folder + " already existed")
            logging.info("The folder " + folder + " already existed")
        # Move the file into the folder that it is designated for
        os.rename(filename, filename.split(".")[0] + "/" + file)


# Puts folders into groups of 25 at a time
def sort_into_groups(size):
    filelist = list_files(sys.argv[1])
    i = 0
    j = 0
    # loop throuch once for each of the files in filelist
    while i < len(filelist) - 1:
        # This splits a path into the filder and the file name
        folder, file = os.path.split(filelist[0])
        # Make the folders to sort everything into
        try:
            os.mkdir(folder + "/" + "folder#" + str(j))
        except:
            print("The folder " + folder + "/" + "folder#" + str(j) + "already exists")
            logging.info("The folder " + folder + "/" + "folder#" + str(j) + "already exists")
        for k in range(size):
            # The while loop is in the wrong place for it to catch an end loop
            # event so it has to be put here
            if len(filelist) <= i:
                break
            # This time we do need file
            folder, file = os.path.split(filelist[i])
            # This does splits the files into the folders
            try:
                os.rename(filelist[i], folder + "/" + "folder#" + str(j) + "/" + file)
            except:
                print("It has already been sorted")
            i += 1
            k += 1
            j += 1


# returns the durration of a audio file
def get_song_length(filename):
    with contextlib.closing(wave.open(filename, 'r')) as f:
        # Easy math... Num of frames / framrate == durration of the song
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def split():
    audio_file_list = list_files(str(sys.argv[1]))
    for audio_file in audio_file_list:
        # Check if it is a wav file
        if(audio_file[-4:] == ".wav"):
            # This is to check if the song has already been cut down
            if get_song_length(audio_file) > 11:
                print ("Splitting " + audio_file + ".")
                logging.info("Splitting " + audio_file + ".")
                # Find how many times it needs to split the audio file
                runs = int(get_song_length(audio_file) / 10)
                # Sets the values so that it can go by 10 second clips
                # In order to chance the number you have to change all the
                # 1000s (done in ms) and the / 10 which is done in seconds
                t1 = 0
                t2 = 10000
                i = 0
                while i < runs:
                    i += 1
                    t1 = t1 + 10000
                    t2 = t2 + 10000
                    # makes the 10 second clips of the audio file
                    newAudio = AudioSegment.from_wav(audio_file)
                    newAudio = newAudio[t1:t2]
                    # exports it as the filename with a the itorator after it
                    newAudio.export(audio_file[:-4] + str(i) + '.wav', format="wav")
                # Deletes source file after the smaller files have been made
                os.remove(audio_file)

                print ("Deleting source file " + audio_file + ".")
                logging.info("Deleting source file " + audio_file + ".")
            else:
                print("\nThe file had already been split")
                logging.info("\nThe file had already been split")


# Currently only works for mp3s, but you can change it to any file type that
# is supported in the library
def convert_to_wav():
    audio_file_list = list_files(str(sys.argv[1]))
    for audio_file in audio_file_list:
        # Filters out any files that are not mp3s
        if audio_file.split('.')[1] == "mp3":
            print("Converting source file " + audio_file + " to .wav")
            logging.info("Converting source file " + audio_file + " to .wav\n")

            # Converts an mp3 file to a wav. You can change some of these values
            # but not everything works
            sound = pydub.AudioSegment.from_mp3(audio_file)
            sound.export(audio_file[:-4] + ".wav", format="wav")

            # Deletes mp3 after the wav has been generated
            os.remove(audio_file)
        else:
            print("\nThe file has already been converted to wav.")
            logging.info("\nThe file has already been converted to wav.")


# Create the spectrograms
def create_spect():
    audioFileList = list_files(sys.argv[1])
    for audioFile in audioFileList:
        if not os.path.isfile(audioFile[:-4] + ".png"):
            millis = time.time()

            # Reports ram and swap space usage for each spectrogram
            logging.info("Creating Spectrogram with " + audioFile + "\n" + str(os.system("free -h")) + "\n")
            print ("Creating Spectrogram with " + audioFile + "\n" + str(os.system("free -h")) + "\n")

            # Creates the spectrogram
            plotstft(audioFile, 1024, audioFile[:-4] + ".png")

            # reports the time that it took to generate the spectrogram
            logging.info("The time is " + str((time.time()) - millis) + "\n\n")
            print("The time is " + str((time.time()) - millis) + "\n\n")


""" The work below this is licensed under a Creative Commons Attribution 3.0 Unported License.
    Frank Zalkow, 2012-2013 """

""" short time fourier transform of audio signal """


def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
    win = window(frameSize)
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))

    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    samples = np.append(np.zeros(np.floor(frameSize / 2.0)), sig)
    # cols for windowing
    cols = np.ceil((len(samples) - frameSize) / float(hopSize)) + 1
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frameSize))

    frames = stride_tricks.as_strided(samples, shape=(cols, frameSize),
                                      strides=(samples.strides[0] * hopSize, samples.strides[0])).copy()
    frames *= win

    return np.fft.rfft(frames)


""" scale frequency axis logarithmically """


def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins - 1) / max(scale)
    scale = np.unique(np.round(scale))

    # create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale) - 1:
            newspec[:, i] = np.sum(spec[:, scale[i]:], axis=1)
        else:
            newspec[:, i] = np.sum(spec[:, scale[i]:scale[i + 1]], axis=1)

    # list center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins * 2, 1. / sr)[:freqbins + 1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale) - 1:
            freqs += [np.mean(allfreqs[scale[i]:])]
        else:
            freqs += [np.mean(allfreqs[scale[i]:scale[i + 1]])]

    return newspec, freqs


""" plot spectrogram"""


def plotstft(audiopath, binsize=2 ** 10, plotpath=None, colormap="jet"):
    samplerate, samples = wav.read(audiopath)
    s = stft(samples, binsize)

    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
    ims = 20. * np.log10(np.abs(sshow) / 10e-6)  # amplitude to decibel

    timebins, freqbins = np.shape(ims)

    plt.figure(figsize=(15, 7.5))
    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()

    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins - 1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins - 1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs * len(samples) / timebins) + (0.5 * binsize)) / samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins - 1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    if plotpath:
        plt.savefig(plotpath, bbox_inches="tight")
    plt.clf()


"""End of his work """

folder, file = os.path.split(sys.argv[1])
logging.basicConfig(filename="logfilename" + str(time.localtime) + ".log", level=logging.INFO)

if sys.argv[2] == "true":
    sort_into_groups(25)
    convert_to_wav()
    split()
else:
    create_spect()
