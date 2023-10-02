import os
import json

# Define the Minecraft profile directory path
appdata_dir = os.environ['APPDATA']
minecraft_dir = os.path.join(appdata_dir, ".minecraft")
profile_name = "CreateNations 1.20.1"
profile_dir = os.path.join(minecraft_dir, profile_name)
profiles_json_path = os.path.join(minecraft_dir, "launcher_profiles.json")
forge_version_dir = os.path.join(minecraft_dir, "versions", "CreateNationsForge")

# Function to create a new profile in the launcher_profiles.json file
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
        # Add other necessary configuration options here
    }

    with open(profiles_json_path, "w") as profiles_file:
        json.dump(profiles_data, profiles_file, indent=4)

def create_forge_version():
    if not os.path.exists(forge_version_dir):
        os.makedirs(forge_version_dir)

    # Create the '1.20.1-forge-47.2.1.json' file with the specified content
    forge_version_file = os.path.join(forge_version_dir, "1.20.1-forge-47.2.1.json")
    forge_version_content = {
        "id": "1.20.1-forge-47.2.1",
        "time": "2023-09-28T07:27:32+00:00",
        "releaseTime": "2023-09-28T07:27:32+00:00",
        "type": "release",
        "mainClass": "cpw.mods.bootstraplauncher.BootstrapLauncher",
        "inheritsFrom": "1.20.1",
        "logging": {},
        "arguments": {
            "game": [
                "--launchTarget",
                "forgeclient",
                "--fml.forgeVersion",
                "47.2.1",
                "--fml.mcVersion",
                "1.20.1",
                "--fml.forgeGroup",
                "net.minecraftforge",
                "--fml.mcpVersion",
                "20230612.114412"
            ],
            "jvm": [
                "-Djava.net.preferIPv6Addresses=system",
                "-DignoreList=bootstraplauncher,securejarhandler,asm-commons,asm-util,asm-analysis,asm-tree,asm,JarJarFileSystems,client-extra,fmlcore,javafmllanguage,lowcodelanguage,mclanguage,forge-,${version_name}.jar",
                "-DmergeModules=jna-5.10.0.jar,jna-platform-5.10.0.jar",
                "-DlibraryDirectory=${library_directory}",
                # Add JVM options and libraries as needed
            ]
        },
        "libraries": [
            {
                "name": "cpw.mods:securejarhandler:2.1.10",
                "downloads": {
                    "artifact": {
                        "path": "cpw/mods/securejarhandler/2.1.10/securejarhandler-2.1.10.jar",
                        "url": "https://maven.minecraftforge.net/cpw/mods/securejarhandler/2.1.10/securejarhandler-2.1.10.jar",
                        "sha1": "51e6a22c6c716beb11e244bf5b8be480f51dd6b5",
                        "size": 88749
                    }
                }
            },
            # Add other required libraries here
        ]
    }

    with open(forge_version_file, "w") as forge_version_json:
        json.dump(forge_version_content, forge_version_json, indent=4)

# Create a new profile in the launcher_profiles.json file
create_new_profile(profiles_json_path, profile_name)

# Create the Forge version JSON file
create_forge_version()

print("Forge version and profile setup completed!")
