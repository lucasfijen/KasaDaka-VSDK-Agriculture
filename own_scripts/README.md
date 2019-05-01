create_wavs.py is used for creating our audio files automatically
using a manually created df and gTTS (google Text To Speech)

We then extend our db_data_backup.json with our newly created wavs and 
automatically add new voice label instances to the django model. We continue with pk's higher than the highest existing df.


Usage:
run create_wavs.py

for local usage:
then from the main folder run:
python manage.py loaddata own_scripts/new_db.json

for server use:
add this folder to the git, and commit
upload to heroku
run: 
- heroku bash
- python manage.py loaddata own_scripts/new_db.json