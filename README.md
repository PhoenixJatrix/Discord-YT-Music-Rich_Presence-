# Discord Rich Presence Python Scripts

This repository contains scripts that interacts with Discord Rich Presence api.

## Youtube Music
Extracts url of the current playing music or even Youtube video from a Chrome tab then using Google's api, it fetches the metadata. The scripts then extracts the artist, title and album cover before updating rich presence. The lifecycle is kept alive with a "while loop" that has a 15 second delay
The title and artist names can be better formatted but this works well enough for my use case

![Screenshot 2025-02-14 215630](https://github.com/user-attachments/assets/ccd0b955-9a8d-4e78-ada9-d71d227de4a1)
![Screenshot 2025-02-14 215751](https://github.com/user-attachments/assets/1279f4d1-876f-4d07-bbde-4e17099e0d93)
![Screenshot 2025-02-14 215656](https://github.com/user-attachments/assets/e5e57d88-88d8-4957-abcf-f1ca95f56177)

### What you need:
#### Python
Python 3.4 or higher
  
  
  
#### Libraries:
- subprocess
- pypresence
- requests
- pathlib
- psutil

You can install the libraries via cmd by typing:
> pip install subprocess
 
> pip install pypresence

> pip install requests

> pip install pathlib

> pip install psutil
  
  
#### Api keys and oauth IDs:
- Discord Application ID. Get it [here](https://discord.com/developers/applications). Create a new application and copy the application ID
   
- Google ApiKey. Watch [this](https://youtu.be/TE66McLMMEw) video or read the official Google guide https://developers.google.com/youtube/v3/getting-started#before-you-start to learn how to get the api key
    
- Path to Google Chrome. Locate the Chrome.exe file then copy the path as is

That's it! You can just run the Python file via cmd or an ide and insert the details and it should open a Chrome instance. From there, open a Youtube Music tab and start playing songs.

You can optionally allow the script to create a Youtube Music shortcut in the desktop. This way, you can easily run the script with just a click (or 2, if you're that specific)
