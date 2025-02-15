# Discord Rich Presence Python Scripts

This repository contains scripts that interacts with Discord Rich Presence api.

## Youtube Music
Extracts url of the current playing music or even Youtube video from a Chrome tab then using Google's api, it fetches the metadata. The scripts then extracts the artist, title and album cover before updating rich presence. The lifecycle is kept alive with a "while loop" that has a 15 second delay
The title and artist names can be better formatted but this works well enough for my use case

![Screenshot 2025-02-14 215630](https://github.com/user-attachments/assets/ccd0b955-9a8d-4e78-ada9-d71d227de4a1)
![Screenshot 2025-02-14 215751](https://github.com/user-attachments/assets/1279f4d1-876f-4d07-bbde-4e17099e0d93)
![Screenshot 2025-02-14 215656](https://github.com/user-attachments/assets/e5e57d88-88d8-4957-abcf-f1ca95f56177)

### What you need:
1. Python 3.4 or higher
   
2. Libraries:
- subprocess
- pypresence
- requests
- pathlib

You can install the libraries via cmd by typing:
> pip install subprocess
> pip install pypresence
> pip install requests
> pip install pathlib

2. Api keys and oauth IDs:
- Discord oauth client ID. Get [here](https://discord.com/developers/applications), then save to [this](https://github.com/PhoenixJatrix/Discord-Rich-Presence-Python-Scripts/blob/main/Youtube%20Music/oauth.txt)(oauth.txt) txt file
- Google ApiKey. Watch [this](https://youtu.be/TE66McLMMEw) video or read the official Google guide https://developers.google.com/youtube/v3/getting-started#before-you-start to learn how to get the api key. When you get the key, save it to [this](https://github.com/PhoenixJatrix/Discord-Rich-Presence-Python-Scripts/blob/main/Youtube%20Music/google_apikey)(google_apikey.txt) txt file
- Path to Google Chrome. Locate the Chrome.exe file then save the path to [this](https://github.com/PhoenixJatrix/Discord-Rich-Presence-Python-Scripts/blob/main/Youtube%20Music/chromepath.txt)(chromepath.txt) txt file

That's it! You can just run the Python file via cmd or an ide and it should work
You can optionally allow the script to create a Youtube Music shortcut in the desktop
