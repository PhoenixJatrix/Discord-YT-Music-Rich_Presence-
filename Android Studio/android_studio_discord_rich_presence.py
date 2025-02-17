import pathlib
import subprocess
import time
import pygetwindow as gw
import pypresence
import os
import psutil

from win32com.client import Dispatch

project = "Deciphering..."
current_tab = "Deciphering..."
thumbnail = "https://cdn.discordapp.com/app-icons/1337221355300720651/1f9e0828106b6dabce6f8bf44ffcd1d1.png?size=64"

buttons = [
    {"label": "Git Repo", "url": "https://github.com/PhoenixJatrix/Discord-Rich-Presence-Python-Scripts"}
]

set_up_details_dir = "C:\\Users\\Public\\Downloads\\Android Studio"
set_up_details_file = f"{set_up_details_dir}\\setup.txt"
bat_path = f"{set_up_details_dir}\\Android Studio.bat"

oauth_client_id = None
studio64_path = None
status_logs = None
current_file_logs = None

status_logs_file = f"{set_up_details_dir}\\log.txt"
current_file_logs_file = f"{set_up_details_dir}\\file_history.txt"

start_time = int(time.time())

# words to capture
targeted_phrases = ["app.main", ".kt"]
# sub strings to remove from the captured titles
clipable_text = ["(:app)", ""]

epochs_before_terminating = 2

def completed_setup() -> bool:
    return os.path.exists(set_up_details_file)

def setup():
    print("\nRead the readme.md file to learn how to get the required keys")
    oauth_input = input("Enter your app's application ID: ")
    studio64_path_input = input("Enter the path to studio64.exe: ")
    create_bin = input("Create a desktop shortcut as 'Android Studio RP' (y|n): ")

    if not os.path.exists(set_up_details_dir):
        os.mkdir(set_up_details_dir)

    if os.path.exists(set_up_details_dir):
        set_up_details = open(set_up_details_file, "w")

        if create_bin.lower() in ["yes", "y"]:
            make_desktop_bat()

        _status_log = open(status_logs_file, "a")
        _current_file_logs = open(current_file_logs_file, "a")

        set_up_details.write(f"{oauth_input}\n{studio64_path_input}")
        set_up_details.close()

        return oauth_input, studio64_path_input, _status_log, _current_file_logs
    else:
        print("set up failed, could not save setup.txt")
        return None

def get_details():
    set_up_details = open(set_up_details_file, "r")
    _oauth_client_id = set_up_details.readline()
    _studio64_path = set_up_details.readline()
    set_up_details.close()

    _status_log = open(status_logs_file, "a")
    _current_file_logs = open(current_file_logs_file, "a")
    return _oauth_client_id, _studio64_path, _status_log, _current_file_logs

def get_title():
    titles = []

    for phrase in targeted_phrases:
        windows = gw.getWindowsWithTitle(phrase)

        if len(windows) != 0:
            titles.append(windows[0])
            break

    return str(titles[0].title) if len(titles) > 0 else None

def clean_title(title: str):
    new_title = title

    if title is None:
        return None

    if "[" in new_title:
        new_title = new_title[:new_title.index("[")]

    for text in clipable_text:
        if text in title:
            new_title = new_title.replace(text, "", 1)

    return new_title

def log_message(message):
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    sec = time.localtime().tm_sec
    time_of_day = "PM" if hour > 12 else "AM"

    if hour > 12:
        hour = hour - 12
    status_logs.write(f"{message} at {f"0{hour}" if hour < 10 else hour}:{f"0{minute}" if minute < 10 else minute}:{f"0{sec}" if sec < 10 else sec} {time_of_day} on {time.localtime().tm_year}:{time.localtime().tm_mon}:{time.localtime().tm_mday}\n\n")


def log_current_file(file_name):
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    sec = time.localtime().tm_sec
    time_of_day = "PM" if hour > 12 else "AM"

    if hour > 12:
        hour = hour - 12
    current_file_logs.write(f"{file_name} at {f"0{hour}" if hour < 10 else hour}:{f"0{minute}" if minute < 10 else minute}:{f"0{sec}" if sec < 10 else sec} {time_of_day} on {time.localtime().tm_year}:{time.localtime().tm_mon}:{time.localtime().tm_mday}\n\n")

def make_desktop_bat():
    if not os.path.exists(bat_path):
        bat_file = open(bat_path, "w")
        bat_file.write(f"@echo off\npython \"{os.path.abspath(__file__)}\"\npause")
        bat_file.close()

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(f"{pathlib.Path.home()}\\Desktop\\Android Studio RP.lnk")
        shortcut.Targetpath = bat_path
        shortcut.IconLocation = f"{pathlib.Path(__file__).parent}\\Android_Studio.ico"
        shortcut.save()

def is_studio64_running() -> bool:
    for pcs_iter in psutil.process_iter():
        if pcs_iter.name() == "studio64.exe":
            return True

    return False

if __name__ == "__main__":
    while True:
        if completed_setup():
            oauth_client_id, studio64_path, status_logs, current_file_logs = get_details()
            log_message(f"initialized")
        else:
            details = setup()

            if details is not None:
                oauth_client_id, studio64_path, status_logs, current_file_logs = details
                log_message(f"first initialization")

        if studio64_path is not None:
            # opening chrome in a debug environment
            process = subprocess.Popen(f"{studio64_path}")

            # create an instance with the client ID
            rich_presence = pypresence.Presence(oauth_client_id)
            rich_presence.connect()
            rich_presence.update(state=project, large_image=thumbnail, buttons=buttons, start=start_time, details=current_tab)

            while True:
                try:
                    cleaned_title = clean_title(get_title())

                    if cleaned_title is not None:
                        epochs_before_terminating = 2
                        new_tab = cleaned_title.split("–")[1].strip()

                        if new_tab != current_tab:
                            project = cleaned_title.split("–")[0].strip()
                            current_tab = cleaned_title.split("–")[1].strip()

                            rich_presence.update(state=project, large_image=thumbnail, start = start_time, large_text="Kotlin", buttons=buttons, small_image="https://drive.usercontent.google.com/download?id=1kNJslXFWz8dWgUWenQG1EZAjuDf7UoB_", small_text="Made by PhoenixJatrix", details=current_tab)
                            log_message("updated rich presence")
                            print("updated rich presence")

                            log_current_file(new_tab)
                    else:
                        if not is_studio64_running():
                            if epochs_before_terminating < 1:
                                log_message("terminated cycle because Android Studio isn't running")
                                print("terminated cycle because Android Studio isn't running")
                                break

                            log_message(f"terminating cycle in {15 * epochs_before_terminating} seconds, Android Studio probably not running")
                            print(f"terminating cycle in {15 * epochs_before_terminating} seconds, Android Studio probably not running")

                            epochs_before_terminating -= 1
                        else:
                            log_message("Current file extension (or name) isn't in targeted phrases")
                            print("Current file extension (or name) isn't in targeted phrases")

                except Exception as e:
                    print(e)
                    log_message(e)

                time.sleep(15)

        if epochs_before_terminating < 1:
            break

        command = input("Encountered an issue. Restart? (y|n): ")

        if command.lower() in ["yes", "y"]:
            print("Restarting")
            log_message("restarting")

            continue
        else:
            log_message("end process")
            break