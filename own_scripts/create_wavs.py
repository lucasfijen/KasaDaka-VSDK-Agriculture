#%%
# For explanation, look at readmy.md in this folder.
import pandas as pd
import json
from gtts import gTTS
from pydub import AudioSegment

import os, glob

df = pd.read_csv('own_scripts/sound_files.csv')
df
folder = 'own_scripts/wavs/'

#%%
for i,row in df.iterrows():
    for lan in ['en', 'fr']:
        tts = gTTS(row[lan], lang=lan)
        tts.save(folder + row['filename'] + '_' + lan + '.mp3')


for file in os.listdir(folder):
    if file.endswith(".mp3"):
        filename = os.path.splitext(file)[0]
        sound = AudioSegment.from_mp3(folder+file)
        sound = sound.set_channels(1)
        sound = sound.set_frame_rate(8000)
        sound.export(folder + filename + '.wav', format="wav", bitrate=16, codec='s16le')
        os.remove(folder+file)

#%%