import os
import json
import shutil
import requests
import subprocess
import zipfile

# Define the Minecraft profile and mods directory paths
appdata_dir = os.environ['APPDATA']
minecraft_dir = os.path.join(appdata_dir, ".minecraft")
profile_name = "CreateNations 1.20.1"
profile_dir = os.path.join(minecraft_dir, profile_name)
mods_dir = os.path.join(profile_dir, "mods")
profiles_json_path = os.path.join(minecraft_dir, "launcher_profiles.json")
new_profiles_json_path = os.path.join(minecraft_dir, "CreateNations1201.json")
new_version_dir = os.path.join(minecraft_dir, "versions", "CreateNations")
new_version_jar_path = os.path.join(new_version_dir, "CreateNations1201.jar")

# Function to create a custom .jar file
def create_custom_jar(new_version_jar_path):
    # Create an empty .jar file (You can customize this part)
    subprocess.run(["jar", "cf", new_version_jar_path])

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
        "type": "custom",
        "custom": new_version_jar_path,  # Set the custom .jar file path
        # Add other necessary configuration options here
    }

    with open(profiles_json_path, "w") as profiles_file:
        json.dump(profiles_data, profiles_file, indent=4)

def create_custom_jar(new_version_jar_path):
    with zipfile.ZipFile(new_version_jar_path, 'w', zipfile.ZIP_DEFLATED) as custom_jar:
        # Add your mod jar files to the custom .jar
        for item in os.listdir(mods_dir):
            item_path = os.path.join(mods_dir, item)
            if os.path.isfile(item_path) and item.endswith(".jar"):
                custom_jar.write(item_path, os.path.basename(item_path))

# Create the Mods folder and copy mod jars
def setup_profile(new_profile_name):
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    # Create a "mods" directory inside the profile folder
    if not os.path.exists(mods_dir):
        os.makedirs(mods_dir)

    # Copy your mod jars to the new profile's "mods" directory
    # Place your mod jar files in a directory, e.g., "CreateNationsMods", and copy them here
    mod_source_dir = os.path.join(appdata_dir, "CreateNationsMods")
    if os.path.exists(mod_source_dir):
        for item in os.listdir(mod_source_dir):
            source_item = os.path.join(mod_source_dir, item)
            dest_item = os.path.join(mods_dir, item)
            if os.path.isfile(source_item):
                shutil.copy2(source_item, dest_item)

if __name__ == "__main__":
    # Ensure that the custom .jar file is created before attempting to copy it
    create_custom_jar(new_version_jar_path)
    create_new_profile(profiles_json_path, profile_name)
    setup_profile(profile_name)