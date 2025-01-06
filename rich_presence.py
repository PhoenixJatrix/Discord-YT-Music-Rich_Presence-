import json
import subprocess
import time
import pypresence
import requests

title = "Deciphering..."
artist = "Made by PhoenixJatrix"
start = int(time.time().real)
end = start + 1
thumbnail = "https://drive.usercontent.google.com/download?id=1kNJslXFWz8dWgUWenQG1EZAjuDf7UoB_"
url = "https://music.youtube.com/"

buttons = [
    {"label": "Listen", "url": url},
    {"label": "Git Repo", "url": "https://github.com/PhoenixJatrix/Discord-YT-Music-Rich_Presence-"},
]

# path to txt file with the discord oauth client ID
o_auth_file = open("C:\\Users\\Public\\Downloads\\discord_oauth.txt")
o_auth_client_id = o_auth_file.readline()
o_auth_file.close()

# path to google api key
google_apikey_file = open("C:\\Users\\Public\\Downloads\\google_apikey.txt")
google_apikey = google_apikey_file.readline()
google_apikey_file.close()

error_log = open("C:\\Users\\Public\\Downloads\\log.txt", "a")

# create an instance with the client ID
rPresence = pypresence.Presence(o_auth_client_id)

rPresence.connect()
rPresence.update(state = title, large_image = thumbnail, buttons = buttons, start = start, end = end, details=artist)

# Chrome.exe path then opening chrome in a debug environment
debugProcess = subprocess.Popen("\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --remote-debugging-port=9222 --user-data-dir=\"C:\\ChromeDebug\"")

time.sleep(5)

def get_tabs():
    response = requests.get("http://localhost:9222/json")
    return response.json()

def kill_process():
    debugProcess.terminate()
    rPresence.close()

def cast_time(time_str: str):
    total_time = 0

    modified_time = time_str.replace("PT", "")

    if "M" in modified_time:
        minutes = modified_time[0:modified_time.find("M")]
        total_time = int(minutes) * 60

    if "S" in modified_time:
        seconds = modified_time[modified_time.find("M") + 1:len(modified_time) - 1]
        total_time += int(seconds)

    return total_time

def log_message(message) :
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    sec = time.localtime().tm_sec
    time_of_day = "PM" if hour > 12 else "AM"

    if hour > 12:
        hour = hour - 12
    error_log.write(f"{message} at {f"0{hour}" if hour < 10 else hour}:{f"0{minute}" if minute < 10 else minute}:{f"0{sec}" if sec < 10 else sec} {time_of_day} on {time.localtime().tm_year}:{time.localtime().tm_mon}:{time.localtime().tm_mday}\n\n")

def extract_id(target_url) -> str:
    if "&" in target_url:
        return updated_url[updated_url.find("=") + 1:updated_url.find("&")]
    else:
        return updated_url[updated_url.find("=") + 1:]

if __name__ == "__main__":
    while True:
        try:
            tabs = list(get_tabs())
            if tabs:
                tab = tabs[0]

                updated_url = str(tab["url"])
                updated_id = extract_id(updated_url)

                req = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={updated_id}&key={google_apikey}")
                reqJson = req.json()

                raw_items = list(json.loads(json.dumps(reqJson["items"])))

                print(f"Raw Items: {raw_items}")

                if len(raw_items) > 0:
                    items = raw_items[0]
                    updated_title = str(items["snippet"]["title"])
                    updated_thumbnail = items["snippet"]["thumbnails"]["default"]["url"]
                    duration = items["contentDetails"]["duration"]
                    updated_artist = str(items["snippet"]["channelTitle"])

                    print(f"Title: {updated_title}")

                    if "-" in updated_title:
                        updated_artist = updated_title[0:updated_title.find("-")].strip()
                        updated_title = updated_title[updated_title.find("-") + 1:].strip()

                    if url != updated_url:
                        title = updated_title
                        start = int(time.time().real)
                        end = start + cast_time(duration)
                        thumbnail = updated_thumbnail
                        artist = updated_artist

                        buttons = [
                            {"label": "Listen", "url": updated_url},
                            {"label": "Git Repo", "url": "https://github.com/PhoenixJatrix/Discord-YT-Music-Rich_Presence-"},
                        ]

                        artist = artist if len(artist) > 2 else f"{artist}   "
                        title = title if len(title) > 2 else f"{title}   "

                        url = updated_url
                        rPresence.update(state=artist, large_image=thumbnail, large_text=title, buttons=buttons, start=start, end=end, small_image="https://drive.usercontent.google.com/download?id=1kNJslXFWz8dWgUWenQG1EZAjuDf7UoB_", small_text="Made by PhoenixJatrix", details=title)
                else:
                    log_message(f"empty metadata for {url}")

            time.sleep(15)
        except Exception as e:
            print(e.args)
            log_message(e)
            #kill_process()
            break