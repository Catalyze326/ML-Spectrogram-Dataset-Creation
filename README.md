This is a ML algorithm that classifies songs by style of dance, although it should work for classifacation of genres.

It uses Spectrograms to use image classifacation on audio files. The field of audio classifacation is fairly untested so this is a way to use a more mature method to classify audio.

It is ment to be used with linux. If you desperately need a windows adaption to it email me at calebmorton98@gmail.com, however if you sue windows I would sugest you use bash on Windows before trying to modify it to work with windows.

It is ment to work with a large quantities of mp3 files which it turns into wav files and then it sorts it into folders of 25 songs. It takes those and splits them into 10 second clips. You can change this, but I found that 10 second clips was the best size because it gives enough of the file to be trained against while having as much to train against as possable. When it finishes the machine learning part it puts these back together to find the most accurite classifacation of a song. After splitting the songs it turns them into spectrograms.

When turning files into spectrograms en masse there seem to be problems with memory where the memory is not flushed after one spectrogram is generated. Because of this I took the easy route and optamized it by writing another script that will run one folder (25 songs) at a time. This is a cheap way of optimization, but it is the best I can do for now.
![alt text](https://github.com/Catalyze326/ML-Spectrogram-Dataset-Creation/blob/master/spectroTest/1024/DropsOfJupiter.png)
