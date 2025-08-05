# CS2 Demo Highlights Project Explanation

## Overview
This project automatically creates highlight videos from CS2 (Counter-Strike 2) demo files. It parses demo files, identifies player kills, and creates video clips of each kill using OBS for recording and CS2's demo playback functionality.

## How It Works
1. Parses CS2 demo files to extract player information and kill events
2. Allows user to select a player and round from the demo
3. Launches CS2 and loads the demo file
4. Uses OBS to record video clips of each kill
5. Combines all clips into a single highlight video

## Key Components
- **main.py**: Main application logic
- **config.py**: Configuration settings
- **util.py**: Utility functions for Steam/CS2 path detection and process management
- **requirements.txt**: Python dependencies

## Dependencies
- PyGetWindow: Window management
- PyAutoGUI: Automation of keyboard/mouse inputs
- pick: Terminal-based selection interface
- obs-websocket-py: OBS automation via WebSocket
- moviepy: Video editing and compilation
- demoparser2: CS2 demo file parsing
- psutil: Process management

## Configuration Options (config.py)

### OBS WebSocket Settings
- `obs_ws_host`: Host address for OBS WebSocket connection (default: "localhost")
- `obs_ws_port`: Port for OBS WebSocket connection (default: 4455)
- `obs_ws_password`: Password for OBS WebSocket authentication (default: "qwertyuiop")

### Timing Settings
- `cs2_load_time`: Time to wait for CS2 to launch (default: 20 seconds)
- `cs2_demo_load_time`: Time to wait for demo to load (default: 10 seconds)

## Other Tweakable Options

### OBS Profile
- The application uses a specific OBS profile named "cs2_demo_highlights"
- Users need to create this profile in OBS with their preferred recording settings

### File Paths
- Demo files should be placed in the same directory as main.py
- Temporary video clips are saved to: `%USERPROFILE%/Videos/cs2_demo_highlights_temp`
- Final videos are saved to: `%USERPROFILE%/Videos/`

### Recording Duration
- Each kill recording lasts for 5 seconds (hardcoded in main.py)
- This duration can be modified in the recording loop

### Video Output Settings
- Output FPS is set to 120 (can be adjusted in the final video compilation)
- Output filename includes player name, kill count, and a random identifier

### CS2 Settings
- Requires borderless fullscreen mode
- Unicode player names are not supported
- Requires proper OBS setup with window capture and WebSocket enabled

## Installation Requirements
1. Python installation
2. OBS Studio with WebSocket plugin
3. Steam with CS2 installed
4. Proper OBS profile configuration

## Usage Workflow
1. Place .dem files in the project directory
2. Configure OBS with the required profile and settings
3. Adjust config.py settings as needed
4. Run the application with `python main.py`
5. Select demo file, player, and round through the terminal interface
6. Wait for the automated process to complete
7. Find the final video in the Videos folder

## Limitations
- Windows-only application
- Requires specific CS2 display mode (borderless fullscreen)
- Does not support Unicode player names
- Requires manual OBS setup
- No GUI - terminal-based interface only

## Potential Improvements
- Add GUI interface
- Support for Unicode player names
- Configurable recording duration per clip
- More flexible file organization
- Cross-platform support
- Better error handling and recovery
- Progress indicators during processing
