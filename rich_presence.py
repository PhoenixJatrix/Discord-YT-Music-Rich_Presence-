import json
import subprocess
import time
import pypresence
import requests

title = "deciphering..."
start = int(time.time().real)
end = start + 1
thumbnail = "https://drive.usercontent.google.com/download?id=1kNJslXFWz8dWgUWenQG1EZAjuDf7UoB_"
url = "https://music.youtube.com/"

buttons = [
    {"label": "Listen", "url": url}
]

# path to txt file with the discord oauth client ID
o_auth_file = open("-- path to your oauth client ID --")
o_auth_client_id = o_auth_file.readline()
o_auth_file.close()

# create an instance with the client ID
rPresence = pypresence.Presence(o_auth_client_id)

rPresence.connect()
rPresence.update(state = title, large_image = thumbnail, buttons = buttons, start = start, end = end)

# Chrome.exe path then opening chrome in a debug environment
debugProcess = subprocess.Popen("-path to chrome.exe- --remote-debugging-port=9222 --user-data-dir=\"C:\\ChromeDebug\"")

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

if __name__ == "__main__":
    while True:
        try:
            tabs = list(get_tabs())
            if tabs:
                tab = tabs[0]

                updated_url = str(tab["url"])

                if "&" in updated_url:
                    updated_id = updated_url[updated_url.find("=") + 1:updated_url.find("&")]
                else:
                    updated_id = updated_url[updated_url.find("=") + 1:]

                req = requests.get(f"https://ytapi.apps.mattw.io/v3/videos?key=foo&quotaUser=QZ78udzWoIjf3TDqixoVjE90ue49lHO6iu5ttU4R&part=snippet%2Cstatistics%2CrecordingDetails%2Cstatus%2CliveStreamingDetails%2Clocalizations%2CcontentDetails%2CpaidProductPlacementDetails%2Cplayer%2CtopicDetails&id={updated_id}&_=1735889182215")
                reqJson = req.json()

                raw_items = json.loads(json.dumps(reqJson["items"]))

                if raw_items:
                    items = raw_items[0]
                    updated_title = items["snippet"]["title"]
                    updated_thumbnail = items["snippet"]["thumbnails"]["default"]["url"]
                    duration = items["contentDetails"]["duration"]
                    channelTitle = str(items["snippet"]["channelTitle"])

                    if channelTitle not in updated_title:
                        updated_title = f"{updated_title} - {channelTitle.replace(" - Topic", "")}"

                    if url != updated_url:
                        title = updated_title
                        start = int(time.time().real)
                        end = start + cast_time(duration)
                        thumbnail = updated_thumbnail

                        buttons = [
                            {"label": "Listen", "url": updated_url}
                        ]

                        url = updated_url
                        rPresence.update(state=title, large_image=thumbnail, large_text="Current song", buttons=buttons, start=start, end=end, small_image="https://drive.usercontent.google.com/download?id=1kNJslXFWz8dWgUWenQG1EZAjuDf7UoB_", small_text="Made by PhoenixJatrix")

            time.sleep(15)
        except Exception as e:
            print(e.args)
            #kill_process()
            break