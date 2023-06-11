import requests
import sys
import os

def download_plugin(plugin_id, download_folder):
    api_url = f"https://api.spiget.org/v2/resources/{plugin_id}"
    download_url = f"https://api.spiget.org/v2/resources/{plugin_id}/download"

    print(f"Fetching plugin information for ID {plugin_id}...")
    response = requests.get(api_url)
    plugin_info = response.json()

    if 'name' not in plugin_info:
        print(f"Plugin with ID {plugin_id} not found.")
        return

    plugin_name = plugin_info['name']
    filename = f"{plugin_name}.jar"
    save_path = os.path.join(download_folder, filename)

    print(f"Downloading plugin '{plugin_name}' with ID {plugin_id}...")
    response = requests.get(download_url)

    with open(save_path, 'wb') as file:
        file.write(response.content)

    print("Download complete.")

if len(sys.argv) < 2:
    print("Usage: python spiget_download.py pluginId [pluginId...]")
    sys.exit(1)

download_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

# Create the "downloads" folder if it doesn't exist
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Loop through the command line arguments and download each plugin
for plugin_id in sys.argv[1:]:
    download_plugin(plugin_id, download_folder)
