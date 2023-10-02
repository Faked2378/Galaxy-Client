import os
import json
import shutil
import requests
import concurrent.futures
import threading
import urllib.request

# Define the Minecraft profile and mods directory paths using %APPDATA%
appdata_dir = os.environ['APPDATA']
minecraft_dir = os.path.join(appdata_dir, ".test")
profile_name = "CreateNations 1.20.1"
profile_dir = os.path.join(minecraft_dir, profile_name)
mods_dir = os.path.join(profile_dir, "Mods")
profiles_json_path = os.path.join(profile_dir, "launcher_profiles.json")
github_api_url = "https://api.github.com/repos/Faked2378/CreateNations/contents/mods"

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

# Download and copy a single file
def download_and_copy_file(file_info):
    file_name, download_url = file_info
    destination_path = os.path.join(mods_dir, file_name)

    # Check if the file already exists
    if os.path.exists(destination_path):
        os.remove(destination_path)

    urllib.request.urlretrieve(download_url, destination_path)
    print(f"Installed: {file_name}")

# Download and copy the contents of the GitHub folder using multiple threads
def setup_profile(new_profile_name):
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    # Create a "Mods" directory inside the profile folder
    if not os.path.exists(mods_dir):
        os.makedirs(mods_dir)

    # Fetch the contents of the GitHub folder using the GitHub API
    response = requests.get(github_api_url)
    if response.status_code == 200:
        contents = response.json()
        files_to_copy = [(os.path.basename(item["name"]), item["download_url"]) for item in contents if item["type"] == "file"]

        # Use a ThreadPoolExecutor to parallelize the file downloads
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(download_and_copy_file, files_to_copy)

    print("Installation completed.")

# Main script execution
if __name__ == "__main__":
    print(f"Starting installation of {profile_name}...")
    create_new_profile(profiles_json_path, profile_name)
    setup_profile(profile_name)
