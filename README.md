
install python 3.9+

create conda env: 
    conda create -n lichess-bot python=3.9

activate conda, install requirements: 
    conda activate lichess-bot && pip install -r requirements.txt

to start the bot: 
    conda activate lichess-bot && python lichess-bot.py

to kill the bot: 
    pkill -f "python lichess-bot.py"
