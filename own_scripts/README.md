create_wavs.py is used for creating our audio files automatically
using a manually created df and gTTS (google Text To Speech)

TODO: automatically input those in db_data_backup.json  
then automatically add new voice label instances to the django model. continue with pk's higher than the highest existing df.


Usage:
update the sound_files.csv
run create_wavs.py
Copy those files to /vsdk/uploads

# NEXT PART DOESNT APPLY YET, STILL NEEDS WAY TO AUTOMATICALLY ADD TO DATABASE
for local usage:
then from the main folder run:
python manage.py loaddata own_scripts/new_db.json

for server use:
add this folder to the git, and commit
upload to heroku
run: 
- heroku bash
- python manage.py loaddata own_scripts/new_db.json