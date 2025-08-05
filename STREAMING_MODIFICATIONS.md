# Streaming Modifications for CS2 Demo Highlights

## Overview
This document explains how to modify the CS2 Demo Highlights project to stream highlights of an entire game for a selected player instead of recording highlights from a single round. The modifications will also enable streaming the content directly instead of saving it to the file system.

## Current Limitations
1. Only processes one round at a time
2. Records video clips to local storage
3. Combines clips into a single file

## Required Changes

### 1. Remove Round Selection
The current code requires selecting a specific round after selecting a player. To stream highlights from the entire game, we need to process all rounds for the selected player.

**In main.py, remove or modify:**
```python
# Remove round selection code:
rounds = sorted(deaths["total_rounds_played"].unique())
round_counts = deaths["total_rounds_played"].value_counts()
round_options = [f"Round {r} ({round_counts[r]} kills)" for r in rounds]
option, index = pick(round_options, "(q to exit) select a round:", quit_keys=[ord("q")], indicator=">")
selected_round = rounds[index]
deaths = deaths[deaths["total_rounds_played"] == selected_round]
```

**Replace with:**
```python
# Process all rounds for the selected player
print(f"Processing all rounds for player {selected_player_name}")
```

### 2. Add Streaming Dependencies
Add streaming libraries to requirements.txt:
```
# For Twitch streaming
twitchio==2.0.0
# For YouTube Live streaming
google-api-python-client==2.0.0
```

### 3. Implement Streaming Functionality
Replace the local recording and video compilation sections with streaming code:

**Replace the recording section:**
```python
# Replace this entire section:
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

# And the video compilation section:
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
```

**With streaming code:**
```python
# Stream each highlight instead of recording locally
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

    # Start streaming instead of recording
    ows_client.call(requests.StartStream())
    
    # Stream for 5 seconds
    time.sleep(5)
    
    # Stop streaming
    ows_client.call(requests.StopStream())
    
    pyautogui.write("`")
    pyautogui.write(f"demo_pause")
    pyautogui.press("enter")
```

### 4. Configure OBS for Streaming
1. Set up OBS with your streaming service (Twitch, YouTube, etc.)
2. Configure stream settings in OBS (keyframes, bitrate, resolution)
3. Add streaming credentials to OBS (stream key)

### 5. Add Streaming Configuration
Create a new section in config.py:
```python
# Streaming settings
stream_service = "twitch"  # or "youtube"
stream_key = "your_stream_key_here"
stream_title = "CS2 Highlights"
stream_description = "Automated CS2 Highlights"
```

### 6. Add Error Handling and Status Updates
Add code to handle streaming errors and provide status updates:
```python
try:
    # Streaming code here
    print(f"Streaming highlight {index+1}/{len(deaths)}")
except Exception as e:
    print(f"Error streaming highlight: {e}")
    # Handle error appropriately
```

## Alternative Approach: RTMP Streaming
Instead of using OBS's built-in streaming, you could:
1. Continue recording short clips with OBS
2. Use ffmpeg-python to stream each clip via RTMP
3. This approach gives more control over the streaming process

## Implementation Considerations

### Timing
- Ensure proper timing between highlights to avoid overlapping streams
- Add delays between highlights for scene transitions

### Stream Quality
- Configure OBS to output at your desired streaming quality
- Consider using different settings for streaming vs. recording

### Error Handling
- Handle cases where streaming fails
- Implement fallback to local recording if streaming fails

### User Interface
- Add option to choose between streaming and recording
- Show streaming status to the user

## Required Code Changes Summary

1. Remove round selection interface
2. Process all deaths for selected player across all rounds
3. Replace local recording with streaming calls
4. Add streaming configuration options
5. Implement error handling for streaming
6. Add status updates during streaming process

## Additional Features to Consider

1. **Live Chat Integration**: Connect to your streaming platform's chat to show reactions
2. **Overlay Information**: Add player stats, kill count, etc. as overlays
3. **Scheduled Streaming**: Automatically start streaming at specific times
4. **Multi-Platform Streaming**: Stream to multiple platforms simultaneously
5. **Highlight Selection**: Allow viewers to vote on which highlights to stream next

## Security Considerations

1. Store stream keys securely (use environment variables)
2. Don't commit stream keys to version control
3. Implement proper authentication for any web interfaces

## Testing

1. Test with a short demo file first
2. Verify stream quality and timing
3. Test error handling scenarios
4. Verify that all highlights are streamed correctly
