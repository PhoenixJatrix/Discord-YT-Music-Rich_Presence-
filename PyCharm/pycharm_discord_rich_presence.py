import subprocess
import time
import pygetwindow as gw
import pypresence

project = "Deciphering..."
current_tab = "Made by PhoenixJatrix"
thumbnail = "https://cdn.discordapp.com/app-icons/1337221355300720651/1f9e0828106b6dabce6f8bf44ffcd1d1.png?size=64"

buttons = [
    {"label": "Git Repo", "url": "https://github.com/PhoenixJatrix/Discord-Rich-Presence-Python-Scripts"}
]

# path to txt file with the discord oauth client ID
o_auth_file = open("oauth.txt")
o_auth_client_id = o_auth_file.readline()
o_auth_file.close()

# path where the log will be saved
error_log = open("log.txt", "a")

# create an instance with the client ID
rPresence = pypresence.Presence(o_auth_client_id)

rPresence.connect()
rPresence.update(state = current_tab, large_image = thumbnail, buttons = buttons, details=project)

# path to PyCharm exe file
pycharm_process = subprocess.Popen("C:\\Program Files\\JetBrains\\PyCharm Community Edition 2024.3.1.1\\bin\\pycharm64.exe")
start_time = int(time.time())

# words to capture
targeted_phrases = [".py"]

# sub strings to remove from the captured titles
clipable_text = []

time.sleep(5)

def kill_process():
    pycharm_process.terminate()
    rPresence.close()

def log_message(message) :
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    sec = time.localtime().tm_sec
    time_of_day = "PM" if hour > 12 else "AM"

    if hour > 12:
        hour = hour - 12
    error_log.write(f"{message} at {f"0{hour}" if hour < 10 else hour}:{f"0{minute}" if minute < 10 else minute}:{f"0{sec}" if sec < 10 else sec} {time_of_day} on {time.localtime().tm_year}:{time.localtime().tm_mon}:{time.localtime().tm_mday}\n\n")

def get_title() -> str:
    titles = []

    for phrase in targeted_phrases:
        windows = gw.getWindowsWithTitle(phrase)

        if len(windows) != 0:
            titles.append(windows[0])
            break

    return str(titles[0].title) if len(titles) > 0 else ""

def clean_title(title: str) -> str:
    new_title = title

    if "[" in new_title:
        new_title = new_title[:new_title.index("[")]

    for text in clipable_text:
        if text in title:
            new_title = new_title.replace(text, "", 1)

    return new_title

if __name__ == "__main__":
    while True:
        try:
            cleaned_title = clean_title(get_title())

            if cleaned_title:
                project = cleaned_title.split("–")[0].strip()
                current_tab = cleaned_title.split("–")[1].strip()

                rPresence.update(state=project, large_image=thumbnail, start=start_time, large_text="Python", buttons=buttons, small_image="https://drive.usercontent.google.com/download?id=1kNJslXFWz8dWgUWenQG1EZAjuDf7UoB_", small_text="Made by PhoenixJatrix", details=current_tab)
                log_message("updated rich presence")
                print("updated rich presence")
            else:
                # log this message 50% of the time to reduce logging
                if time.time() % 2 == 0:
                    log_message("PyCharm probably not running or current file isn't listed in targeted phrases")
                print("PyCharm probably not running or current file isn't listed in targeted phrases")

        except Exception as e:
            print(e)
            log_message(e)

        time.sleep(15)