import os
import requests
import shutil
import sys
import subprocess

# Get the Minecraft version from the command-line argument or use the default value
minecraft_version = sys.argv[1] if len(sys.argv) > 1 else "1.19.4"

# Create the server folder if it doesn't exist
server_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "servers")
os.makedirs(server_folder, exist_ok=True)

# Create the eula.txt file with eula=true
eula_file = os.path.join(server_folder, "eula.txt")
with open(eula_file, "w") as file:
    file.write("eula=true\n")

# Check if the "copy" argument is provided, copy files to "./servers/plugins" if it exists
if "copy" in sys.argv:
    downloads_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
    if os.path.exists(downloads_folder):
        # Check if the Minecraft version argument is provided, then fetch and download the PurpurMC server
        if minecraft_version != "copy":
            # Fetch the download URL for the specified PurpurMC build
            purpurmc_url = f"https://api.purpurmc.org/v2/purpur/{minecraft_version}/latest/download"
            response = requests.get(purpurmc_url, stream=True)
            response.raise_for_status()

            # Set the destination file path
            purpurmc_file = os.path.join(server_folder, "server.jar")

            # Download the PurpurMC server JAR
            with open(purpurmc_file, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            print(f"PurpurMC for Minecraft {minecraft_version} downloaded successfully!")

        # Check if the "plugins" directory exists in the server folder, create it if necessary
        plugins_folder = os.path.join(server_folder, "plugins")
        os.makedirs(plugins_folder, exist_ok=True)

        # Copy files from "./downloads" to "./servers/plugins"
        for filename in os.listdir(downloads_folder):
            source_file = os.path.join(downloads_folder, filename)
            destination_file = os.path.join(plugins_folder, filename)
            shutil.copy(source_file, destination_file)
            print(f"File '{filename}' copied to './servers/plugins'")
    else:
        print("No files to copy. 'downloads' directory does not exist.")
else:
    print("No files copied. 'copy' argument not provided.")

# Check if the "run" argument is provided, run the Minecraft server with fixed RAM allocation of 2GB
if "run" in sys.argv:
    # Start the Minecraft server with fixed RAM allocation of 2GB
    command = ["java", "-Xmx2G", "-jar", "server.jar"]
    subprocess.Popen(command, cwd=server_folder)
    print("Minecraft server started with 2GB RAM allocation.")
else:
    print("Minecraft server not started. 'run' argument not provided.")
