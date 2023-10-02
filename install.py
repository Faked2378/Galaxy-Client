import os
import json
import shutil

# Define the Minecraft profile and mods directory paths
minecraft_dir = "C:\\Users\\marek\\Desktop\\test"
profile_name = "CreateNations 1.20"
profile_dir = os.path.join(minecraft_dir, profile_name)
profiles_json_path = os.path.join(profile_dir, "launcher_profiles.json")
mods_dir = os.path.join(minecraft_dir, "mods")

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
        "gameDir": os.path.join(minecraft_dir, new_profile_name),
        "lastVersionId": "1.20",
        "javaArgs": "-Xmx2G -Xms1G",
        # Add other necessary configuration options here
    }

    with open(profiles_json_path, "w") as profiles_file:
        json.dump(profiles_data, profiles_file, indent=4)

# Create a directory for the new profile and copy mods
def setup_profile(new_profile_name):
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    # Copy your mods to the new profile's mods directory
    # You should place your mod files in a directory, e.g., "CreateNationsMods", and copy them here
    mod_source_dir = os.path.join(minecraft_dir, "CreateNationsMods")
    if os.path.exists(mod_source_dir):
        shutil.copytree(mod_source_dir, os.path.join(profile_dir, "mods"))

# Main script execution
create_new_profile(profiles_json_path, profile_name)
setup_profile(profile_name)
