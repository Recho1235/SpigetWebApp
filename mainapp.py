import os
import subprocess
from flask import Flask, render_template, request, send_from_directory, send_file, redirect, url_for

app = Flask(__name__)
download_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

def download_plugin(plugin_id):
    try:
        command = ['python', 'spiget_download.py', plugin_id]
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_plugin_exists(plugin_id):
    plugin_jar = f"{plugin_id}.jar"
    return plugin_jar in os.listdir(download_folder)

def check_plugin_status(plugin_id):
    initial_files = set(os.listdir(download_folder))
    if download_plugin(plugin_id):
        final_files = set(os.listdir(download_folder))
        if final_files - initial_files:
            return 'success'
    return 'not_found'

@app.route('/', methods=['GET', 'POST'])
def index():
    download_status = None
    if request.method == 'POST':
        plugin_id = request.form['plugin_id']
        if plugin_id:
            download_status = check_plugin_status(plugin_id)
    return render_template('index.html', download_status=download_status)


@app.route('/downloads')
def downloads():
    files = os.listdir(download_folder)
    return render_template('downloads.html', files=files)

@app.route('/downloads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(download_folder, filename, as_attachment=True)

@app.route('/delete_file', methods=['GET'])
def delete_file():
    filename = request.args.get('filename', '')
    filepath = os.path.join(download_folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('downloads'))

if __name__ == '__main__':
    app.run()
