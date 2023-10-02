import os
import json
import shutil
import requests

# Define the Minecraft profile and mods directory paths using %APPDATA%
appdata_dir = os.environ['APPDATA']
minecraft_dir = os.path.join(appdata_dir, ".test")
profile_name = "CreateNations 1.20.1"
profile_dir = os.path.join(minecraft_dir, profile_name)
mods_dir = os.path.join(profile_dir, "Mods")
profiles_json_path = os.path.join(profile_dir, "launcher_profiles.json")
github_mods_folder_url = "https://github.com/Faked2378/CreateNations/tree/main/mods/"

# Create a new profile in the launcher_profiles.json file
def create_new_profile(profiles_json_path, new_profile_name):
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    if not os.path.exists(profiles_json_path):
        # Create an empty launcher_profiles.json if it doesn't exist
        with open(profiles_json_path, "w") as profiles_file:
            json.dump({}, profiles_file)

    with open(profiles_json_path, "r") as profiles_file:
        profiles_data = json.load(profiles_file)

    # Check if "profiles" key exists; if not, create it
    if "profiles" not in profiles_data:
        profiles_data["profiles"] = {}

    profiles_data["profiles"][new_profile_name] = {
        "name": new_profile_name,
        "gameDir": profile_dir,
        "lastVersionId": "1.20.1",
        "javaArgs": "-Xmx2G -Xms1G",
        # Add other necessary configuration options here
    }

    with open(profiles_json_path, "w") as profiles_file:
        json.dump(profiles_data, profiles_file, indent=4)

# Download the contents of the GitHub folder and copy them to the "Mods" directory
def setup_profile(new_profile_name):
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    # Create a "Mods" directory inside the profile folder
    if not os.path.exists(mods_dir):
        os.makedirs(mods_dir)

    # Download the contents of the GitHub folder and copy them to "Mods"
    response = requests.get(github_mods_folder_url)
    if response.status_code == 200:
        # Parse the HTML response to extract file/folder links
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        # Filter and download the contents of the folder
        for link in links:
            href = link.get('href')
            if href.startswith('/Faked2378/CreateNations/tree/main/mods/'):
                file_name = os.path.basename(href.rstrip('/'))
                download_url = f'https://raw.githubusercontent.com{href}/'
                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(os.path.join(mods_dir, file_name), 'wb') as file:
                        file.write(response.content)

# Main script execution
create_new_profile(profiles_json_path, profile_name)
setup_profile(profile_name)
