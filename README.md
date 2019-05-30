# Spectrogram Dataset Creation
This will be a ML algorithm that classifies songs by style of dance, although it should work for classification of genres as well. For now it only compiles the dataset.

It uses spectrograms to use image classification on audio files. The field of audio classification is fairly untested so this is a way to use a more mature method to classify audio.

This is an example of what the program currently creates. This is a part of the song Drops of Jupiter by Train.
![alt text](https://github.com/Catalyze326/ML-Spectrogram-Dataset-Creation/blob/master/Spectrograms/DropsOfJupiter.png)


# Install Dependencies
````
pip3 install numpy scipy matplotlib pydub 
````
# Running instructions
````
python3 createSpectrogram.py /path/to/music
````