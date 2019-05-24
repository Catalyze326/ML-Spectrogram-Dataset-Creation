#Spectrogram Dataset Creation
This will be a ML algorithm that classifies songs by style of dance, although it should work for classification of genres as well.

It uses Spectrograms to use image classification on audio files. The field of audio classification is fairly untested so this is a way to use a more mature method to classify audio.

This branch is multithreads everything except for moving files between directories. Converting to wav, splitting the files, and creating the spectrograms are all multithreaded.

This is an example of what the program currently creates. This is a part of the song Drops of Jupiter by Train.
![alt text](https://github.com/Catalyze326/ML-Spectrogram-Dataset-Creation/blob/master/Spectrograms/DropsOfJupiter.png)

It is meant to be used with Linux. If you desperately need a windows adaption to it email me at calebmorton98@gmail.com, however if you sue windows, I would suggest you use bash on Windows before trying to modify it to work with windows.

It is meant to work with a large quantities of mp3 files which it turns into wav files and then it sorts it into folders of 25 songs. It takes those and splits them into 10 second clips. You can change this, but I found that 10 second clips were the best size because it gives enough of the file to be trained against while having as much to train against as possible. When it finishes the machine learning part it puts these back together to find the most accurate classification of a song. After splitting the songs, it turns them into spectrograms.

When turning files into spectrograms en masse there seem to be problems with memory where the memory is not flushed after one spectrogram is generated. Because of this I took the easy route and optimized it by writing another script that will run one folder (25 songs) at a time. This is a cheap way of optimization, but it is the best I can do for now.

#Install Dependencies
````
pip3 install numpy scipy matplotlib pydub 
````
#Running instructions
````
python3 createSpectrogram.py /path/to/music
````