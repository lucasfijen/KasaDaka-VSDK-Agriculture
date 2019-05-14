from vsdk.service_development.models import *
import pandas as pd
import json
from gtts import gTTS
from pydub import AudioSegment

import os, glob

# To Run: perform python manage.py runscript populate_db
def run():
    # Read db
    df = pd.read_csv('scripts/sound_files.csv')
    folder = 'vsdk/uploads/'
    print('Performing text to speech')
    for i,row in df.iterrows():
        for lan in ['en', 'fr']:
            tts = gTTS(row[lan], lang=lan)
            tts.save(folder + row['filename'] + '_' + lan + '.mp3')

    # Converting to wavs
    print('converting to wavs')
    for file in os.listdir(folder):
        if file.endswith(".mp3"):
            filename = os.path.splitext(file)[0]
            sound = AudioSegment.from_mp3(folder+file)
            sound = sound.set_channels(1)
            sound = sound.set_frame_rate(8000)
            sound.export(folder + filename + '.wav', format="wav", bitrate=16, codec='s16le')
            os.remove(folder+file)
    
    # Creating files into database
    print('Creating files')
    en = Language.objects.get(pk=2)
    fr = Language.objects.get(pk=3)
    for i, row in df[df.exists == 0].iterrows():
        label, c = VoiceLabel.objects.get_or_create(name = row.filename)
        if c:
            print('Added to db: ', label)
            e = VoiceFragment(parent = label, \
                                language = en, \
                                audio = row.filename + '_en.wav')
            e.save()

            f = VoiceFragment(parent = label, \
                                language = fr, \
                                audio = row.filename + '_fr.wav')
            f.save()