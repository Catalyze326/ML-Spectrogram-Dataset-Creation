# import timeside
# from timeside import Decoder, Spectrogram
import os
import sys
from pydub import AudioSegment
import pydub
import wave
import contextlib
from timeside.core import get_processor


# def graph_spectrogram(wav_file):
#     sound_info, frame_rate = get_wav_info(wav_file)
#     pylab.figure(num=None, figsize=(16, 9))
#     pylab.subplot(111)
#     pylab.title('spectrogram of %r' % wav_file)
#     pylab.specgram(sound_info, Fs=frame_rate)
#     pylab.savefig(wav_file[:-4] + '.png')
#
#
# def get_wav_info(wav_file):
#     wav = wave.open(wav_file, 'r')
#     frames = wav.readframes(-1)
#     sound_info = pylab.fromstring(frames, 'Int16')
#     frame_rate = wav.getframerate()
#     wav.close()
#     return sound_info, frame_rate


def getFileLength(filename):
    with contextlib.closing(wave.open(filename,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return(duration)


def listFiles(loc):
    filelist = []
    for path, dirs, files in os.walk(loc):
        for d in dirs:
            print(path + "//" + d)
        for f in files:
            lol = (path + "//" + f)
            filelist.append(lol)
    print filelist
    print loc
    return filelist


# def createSpect():
#     audio_file_list = listFiles(str(sys.argv[2]))
#     for audio_file in audio_file_list:
#         # decoder = timeside.decoder.FileDecoder(audio_file)
#         # grapher = timeside.grapher.Spectrogram(width=1920, height=1080)
#         # (decoder | grapher).run()
#         # grapher.render(audio_file[:-4] + '.png')
#         graph_spectrogram(audio_file)


def chop():
    # Cut it into 10 second clips
    audio_file_list = listFiles(str(sys.argv[2]))
    for audio_file in audio_file_list:
        print audio_file
        runs = int(getFileLength(audio_file) / 10)
        t1 = 0
        t2 = 10000
        i = 0
        while i < runs:
            i += 1
            t1 = t1 + 10000 #Works in milliseconds
            t2 = t2 + 10000
            newAudio = AudioSegment.from_wav(audio_file)
            newAudio = newAudio[t1:t2]
            newAudio.export(audio_file[:-4] + str(i) + '.wav', format="wav") #Exports to a wav file in the current
            print audio_file[:-4] + str(i) + '.wav'


def convertToWAV():
    print "Convert"
    audio_file_list = listFiles(str(sys.argv[2]))
    for audio_file in audio_file_list:
        print "Converting " + audio_file + "to wav."
        sound = pydub.AudioSegment.from_mp3(audio_file)
        sound.export(audio_file[:-4] + ".wav", format="wav")


def createSpect():
    audio_file_list = listFiles(str(sys.argv[2]))
    for audio_file in audio_file_list:
        decoder = get_processor('file_decoder')(audio_file)
        spectrogram = get_processor('spectrogram_lin')(width=1920, height=1080)
        (decoder | spectrogram).run()
        spectrogram.render('graph.png')


if sys.argv[1] == "--convert2wav":
    convertToWAV()
else:
    if sys.argv[1] == "--chop":
        chop()
    else:
        if sys.argv[1] == "--createSpectrogram":
            createSpect()