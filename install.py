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
    # Ensure that the required directories exist
    os.makedirs(os.path.dirname(new_version_jar_path), exist_ok=True)

    with zipfile.ZipFile(new_version_jar_path, 'w', zipfile.ZIP_DEFLATED) as custom_jar:
        # Add your mod jar files to the custom .jar
        for item in os.listdir(mods_dir):
            item_path = os.path.join(mods_dir, item)
            if os.path.isfile(item_path) and item.endswith(".jar"):
                custom_jar.write(item_path, os.path.basename(item_path))

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
        "lastVersionId": "release 1.20.1-forge-47.2.1",
        "javaArgs": "-Xmx2G -Xms1G",
        "type": "custom",
        "custom": new_version_jar_path,  # Set the custom .jar file path
        # Add other necessary configuration options here
    }

    with open(profiles_json_path, "w") as profiles_file:
        json.dump(profiles_data, profiles_file, indent=4)

# Create the Mods folder and copy mod jars
def setup_profile(new_profile_name):
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    # Create a "mods" directory inside the profile folder if it doesn't exist
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

def create_forge_version():
    forge_version_dir = os.path.join(minecraft_dir, "versions", "CreateNationsForge")
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
        "inheritsFrom": "1.20.1-forge-47.2.1",
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
                "-p",
                "${library_directory}/cpw/mods/bootstraplauncher/1.1.2/bootstraplauncher-1.1.2.jar${classpath_separator}${library_directory}/cpw/mods/securejarhandler/2.1.10/securejarhandler-2.1.10.jar${classpath_separator}${library_directory}/org/ow2/asm/asm-commons/9.5/asm-commons-9.5.jar${classpath_separator}${library_directory}/org/ow2/asm/asm-util/9.5/asm-util-9.5.jar${classpath_separator}${library_directory}/org/ow2/asm/asm-analysis/9.5/asm-analysis-9.5.jar${classpath_separator}${library_directory}/org/ow2/asm/asm-tree/9.5/asm-tree-9.5.jar${classpath_separator}${library_directory}/org/ow2/asm/asm/9.5/asm-9.5.jar${classpath_separator}${library_directory}/net/minecraftforge/JarJarFileSystems/0.3.19/JarJarFileSystems-0.3.19.jar",
                "--add-modules",
                "ALL-MODULE-PATH",
                "--add-opens",
                "java.base/java.util.jar=cpw.mods.securejarhandler",
                "--add-opens",
                "java.base/java.lang.invoke=cpw.mods.securejarhandler",
                "--add-exports",
                "java.base/sun.security.util=cpw.mods.securejarhandler",
                "--add-exports",
                "jdk.naming.dns/com.sun.jndi.dns=java.naming"
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
            {
                "name": "org.ow2.asm:asm:9.5",
                "downloads": {
                    "artifact": {
                        "path": "org/ow2/asm/asm/9.5/asm-9.5.jar",
                        "url": "https://maven.minecraftforge.net/org/ow2/asm/asm/9.5/asm-9.5.jar",
                        "sha1": "dc6ea1875f4d64fbc85e1691c95b96a3d8569c90",
                        "size": 121863
                    }
                }
            },
            {
                "name": "org.ow2.asm:asm-commons:9.5",
                "downloads": {
                    "artifact": {
                        "path": "org/ow2/asm/asm-commons/9.5/asm-commons-9.5.jar",
                        "url": "https://maven.minecraftforge.net/org/ow2/asm/asm-commons/9.5/asm-commons-9.5.jar",
                        "sha1": "19ab5b5800a3910d30d3a3e64fdb00fd0cb42de0",
                        "size": 72209
                    }
                }
            },
            {
                "name": "org.ow2.asm:asm-tree:9.5",
                "downloads": {
                    "artifact": {
                        "path": "org/ow2/asm/asm-tree/9.5/asm-tree-9.5.jar",
                        "url": "https://maven.minecraftforge.net/org/ow2/asm/asm-tree/9.5/asm-tree-9.5.jar",
                        "sha1": "fd33c8b6373abaa675be407082fdfda35021254a",
                        "size": 51944
                    }
                }
            },
            {
                "name": "org.ow2.asm:asm-util:9.5",
                "downloads": {
                    "artifact": {
                        "path": "org/ow2/asm/asm-util/9.5/asm-util-9.5.jar",
                        "url": "https://maven.minecraftforge.net/org/ow2/asm/asm-util/9.5/asm-util-9.5.jar",
                        "sha1": "64b5a1fc8c1b15ed2efd6a063e976bc8d3dc5ffe",
                        "size": 91076
                    }
                }
            },
            {
                "name": "org.ow2.asm:asm-analysis:9.5",
                "downloads": {
                    "artifact": {
                        "path": "org/ow2/asm/asm-analysis/9.5/asm-analysis-9.5.jar",
                        "url": "https://maven.minecraftforge.net/org/ow2/asm/asm-analysis/9.5/asm-analysis-9.5.jar",
                        "sha1": "490bacc77de7cbc0be1a30bb3471072d705be4a4",
                        "size": 33978
                    }
                }
            },
            # Add other required libraries here
        ]
    }

    with open(forge_version_file, "w") as forge_version_json:
        json.dump(forge_version_content, forge_version_json, indent=4)

# Create the custom .jar file
# create_custom_jar(new_version_jar_path)  # Comment out this line

# Create a new profile in the launcher_profiles.json file
create_new_profile(profiles_json_path, profile_name)

# Create the Mods folder and copy mod jars
setup_profile(profile_name)

# Create the Forge version JSON file
create_forge_version()

print("Forge version and profile setup completed!")
