from pick import pick
import os
import shutil
import subprocess
import pygetwindow as gw
import pyautogui
import time
from obswebsocket import obsws, requests
import util
from demoparser2 import DemoParser
import config
from moviepy import *
import uuid

ows_client = obsws(config.obs_ws_host, config.obs_ws_port, config.obs_ws_password)
ows_client.connect()

demos = [f for f in os.listdir() if f.endswith(".dem")]
if not demos:
    print("no demos found!")
    exit(0)
else:
    demo_file, _ = pick(demos, "(q to exit) select a demo file:", quit_keys=[ord("q")], indicator=">")
    if demo_file is None:
        print("no demo selected.")
        exit(0)

parser = DemoParser(str(demo_file).strip())

players = parser.parse_player_info()

deaths = parser.parse_event("player_death", player=["last_place_name", "team_name"], other=["total_rounds_played", "is_warmup_period"])

deaths = deaths[deaths["is_warmup_period"] == False]
players_array = [f"{row['name']} ({ row['steamid']}) ({len(deaths[deaths['attacker_steamid'] == str(row['steamid'])])} kills)" for _, row in players.iterrows()]

if not players_array:
    print("no players found???")
    exit(0)
else:
    player_option, player_index = pick(players_array, "(q to exit) select a player:", quit_keys=[ord("q")], indicator=">")
    if player_option is None:
        print("no player selected.")
        exit(0)

selected_steamid = players['steamid'][player_index]
selected_player_name = players.loc[players['steamid'] == selected_steamid, 'name'].values[0]

deaths = deaths[deaths["attacker_steamid"] == str(selected_steamid)]

if deaths.empty:
    print("no kills found for that player outside warmup")
    exit(0)

rounds = sorted(deaths["total_rounds_played"].unique())

if not rounds:
    print("no rounds with kills found for that player outside warmup")
    exit(0)

round_counts = deaths["total_rounds_played"].value_counts()

round_options = [f"Round {r} ({round_counts[r]} kills)" for r in rounds]

option, index = pick(round_options, "(q to exit) select a round:", quit_keys=[ord("q")], indicator=">")

if option is None:
    print("no round selected.")
    exit(0)

selected_round = rounds[index]

deaths = deaths[deaths["total_rounds_played"] == selected_round]

kills = [f"Kill to {d['user_name']} (tick {d['tick']})" for _, d in deaths.iterrows()]

shutil.copy(demo_file, os.path.join(util.get_cs2_path(), "game", "csgo", "replays"))

if not util.is_cs2_running():
    subprocess.Popen([os.path.join(util.get_steam_path(), "steam.exe"), "-applaunch", "730"])
    print(f"waiting {config.cs2_load_time}s for cs2 to launch")
    time.sleep(config.cs2_load_time)
else:
    print("cs2 already running")

windows = gw.getWindowsWithTitle('Counter-Strike 2')

if windows:
    win: gw.Window = windows[0]
    win.minimize()
    win.restore()
    time.sleep(1)
    pyautogui.click(win.center)
else:
    print("window not found within 20s!")
    exit(0)

ows_client.call(requests.SetCurrentProfile(profileName="cs2_demo_highlights"))
user_videos = os.path.join(os.environ["USERPROFILE"], "Videos", "cs2_demo_highlights_temp")
os.makedirs(user_videos, exist_ok=True)
ows_client.call(requests.SetRecordDirectory(recordDirectory=user_videos))

pyautogui.write("`")
pyautogui.write(f"playdemo replays/{demo_file}")
pyautogui.press("enter")

print(f"Waiting {config.cs2_demo_load_time}s for demo to load!")
time.sleep(config.cs2_demo_load_time)

pyautogui.write("``")
pyautogui.write("demoui")
pyautogui.press("enter")

for _, kill in deaths.iterrows():
    pyautogui.write("``")
    pyautogui.write(f"demo_gototick {kill['tick'] - 200}")
    pyautogui.press("enter")

    selected_name = players.iloc[player_index]['name']
    pyautogui.write(f'spec_player "{selected_name}"')
    pyautogui.press("enter")

    pyautogui.write(f"demo_resume")
    pyautogui.press("enter")
    pyautogui.write("`")

    time.sleep(0.1)

    ows_client.call(requests.StartRecord())

    time.sleep(5)

    ows_client.call(requests.StopRecord())

    pyautogui.write("`")
    pyautogui.write(f"demo_pause")
    pyautogui.press("enter")

pyautogui.write("disconnect")
pyautogui.press("enter")
pyautogui.write("`")

folder = os.path.join(os.environ["USERPROFILE"], "Videos", "cs2_demo_highlights_temp")

clips = []
for file in sorted(os.listdir(folder)):
    if file.lower().endswith((".mp4")):
        path = os.path.join(folder, file)
        clip = VideoFileClip(path)
        clips.append(clip)

final_clip = concatenate_videoclips(clips)
random_str = str(uuid.uuid4())[:8]
final_clip.write_videofile(os.path.join(os.environ["USERPROFILE"], "Videos", f"cs2_demo_highlights - {selected_player_name} - {len(deaths)} kills - {random_str}.mp4"), fps=120)

# cleanup
for clip in clips:
    clip.close()
final_clip.close()

shutil.rmtree(folder)