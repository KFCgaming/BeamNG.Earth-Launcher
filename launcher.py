import requests
import os
import json 
from colorama import Fore, Style
import time
import sys

# Target directory for the executable
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INFO_PATH = os.path.join(BASE_DIR, "info.txt")

def launch():
    if not os.path.exists(INFO_PATH):
        print(Fore.LIGHTRED_EX + "Error: info.txt not found.")
        return

    with open(INFO_PATH, "r") as f:
        verloc = f.readline().strip()
        dataloc = f.readline().strip()
        nameapploc = f.readline().strip()

    app_path = os.path.join(BASE_DIR, nameapploc)
    
    print(Fore.CYAN + f"Launching {nameapploc}...")
    os.system(f'start "" "{app_path}"')
    time.sleep(4)


def downloader():
    with open(INFO_PATH, "r") as f:
        verloc = f.readline().strip()
        dataloc = f.readline().strip()
        nameapploc = f.readline().strip()
    
    # 1. Download latest version from GitHub
    url = "https://api.github.com/repos/TecnaGamer/BeamNG.Earth/releases/latest"
    response = requests.get(url)
    data = response.json()
    vergit = data["tag_name"]
    dategit = data["published_at"]
    nameappgit = data["assets"][1]["name"]
    appurl = data["assets"][1]["browser_download_url"]

    # Chemin complet pour sauvegarder le fichier dans le même dossier que le .exe
    app_path = os.path.join(BASE_DIR, nameappgit)

    print(Fore.LIGHTYELLOW_EX + f"Downloading {nameappgit}...")
    response = requests.get(appurl)
    with open(app_path, "wb") as f:
        f.write(response.content)
    
    # 2. Save info in the txt file
    with open(INFO_PATH, "w") as f:
        f.write(f"{vergit}\n{dategit}\n{nameappgit}")

    # 3. Delete old version
    if os.path.exists(os.path.join(BASE_DIR, nameapploc)):
        os.remove(os.path.join(BASE_DIR, nameapploc))
    else:
        pass
    
    # 4. Launch
    print(Fore.LIGHTGREEN_EX + "Update downloaded! \n")
    checkupdate()

def checkupdate():
    # 1. Check update from txt file (local version)
    if not os.path.exists(INFO_PATH):
        print(Fore.LIGHTRED_EX + "First-time launch. Downloading latest version...")
        downloader()
        return
    
    with open(INFO_PATH, "r") as f:
        verloc = f.readline().strip()
        dataloc = f.readline().strip()
        nameapploc = f.readline().strip()
    
    # 2. Check update from github
    url = "https://api.github.com/repos/TecnaGamer/BeamNG.Earth/releases/latest"
    response = requests.get(url)
    data = response.json()
    vergit = data["tag_name"]
    dategit = data["published_at"]
    nameappgit = data["assets"][1]["name"]

    # 3. Compare versions
    if nameappgit == nameapploc:                  # Launching
        print(Fore.LIGHTGREEN_EX + "Local version: " + nameapploc + Fore.RESET + " | " + Fore.GREEN + "GitHub version: " + nameappgit)
        print(Fore.CYAN + "Launching...")
        launch()
    else:
        print(Fore.LIGHTYELLOW_EX + "Local version: " + nameapploc + Fore.RESET + " | " + Fore.GREEN + "GitHub version: " + nameappgit)
        print(Fore.LIGHTRED_EX + "Update available! Downloading... \n\n ") # Download latest version
        downloader()


# MAIN
print(Fore.LIGHTRED_EX + """
█▄▄ █▀▀ ▄▀█ █▀▄▀█ ░ █▄░█ █▀▀   █▀▀ ▄▀█ █▀█ ▀█▀ █░█   █░░ ▄▀█ █░█ █▄░█ █▀▀ █░█ █▀▀ █▀█
█▄█ ██▄ █▀█ █░▀░█ ▄ █░▀█ █▄█   ██▄ █▀█ █▀▄ ░█░ █▀█   █▄▄ █▀█ █▄█ █░▀█ █▄▄ █▀█ ██▄ █▀▄\n\n""")

checkupdate()