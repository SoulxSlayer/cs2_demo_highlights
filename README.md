# cs2_demo_highlights 🎥

> [!IMPORTANT]  
> Use borderless fullscreen in CS2 for the app to work.
> This app only works on Windows!
> Make sure to properly set up OBS.

## Installation

1. install python
2. download this repo
3. open a cmd / powershell
4. `pip install -r requirements.txt`
5.  tweak config.py (adjust cs2 load & demo load times if needed)

## OBS Setup

1. create a new profile, call it cs2_demo_highlights
2. setup your OBS encoder, resolution, framerate, etc.
3. add a window capture source for cs2, **disable cursor capture**
4. enable websocket: tools > websocket server settings > enable it, set a password
5. update config.py w/ your websocket password + port

## Usage
1. open cmd / powershell window in the folder where you extracted the downloaded archive.
2. put your demo files in the same folder where main.py is
3. run `python main.py`
4. go through the prompts
5. wait for cs2 to launch and don't touch anything until the process is finished (disconnects from the demo player)

## Credits
This code uses the following libraries:
- [PyGetWindow](https://github.com/asweigart/PyGetWindow)
- [PyAutoGUI](https://github.com/asweigart/pyautogui)
- [pick](https://github.com/aisk/pick)
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py)
- [moviepy](https://github.com/Zulko/moviepy)
- [demoparser2](github.com/LaihoE/demoparser)

## Contributing

i'm aware that this code is garbage, so feel free to fork this repo and do some changes and send a pull request back.
