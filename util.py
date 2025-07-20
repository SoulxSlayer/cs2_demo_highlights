import winreg
import os
import psutil

def get_steam_path():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam") as key:
        steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
        return steam_path
    
def get_cs2_path(): # assume CS2 is installed where Steam is
    return os.path.join(get_steam_path(), "steamapps", "common", "Counter-Strike Global Offensive")

def is_cs2_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and "cs2.exe" in proc.info['name'].lower():
            return True
    return False