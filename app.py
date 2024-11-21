from flask import Flask, render_template, request, redirect, url_for, flash
import os
import shutil

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# Function implementations from your file management system
def create_directory(directory_name):
    """Create a new directory"""
    try:
        os.makedirs(directory_name)
        flash(f"Directory '{directory_name}' created successfully.", "success")
    except FileExistsError:
        flash(f"Directory '{directory_name}' already exists.", "error")

def create_file(file_path, content=""):
    """Create a new file with optional content"""
    with open(file_path, 'w') as file:
        file.write(content)
    flash(f"File '{file_path}' created successfully.", "success")

def list_directory(path='.'):
    """List all files and directories in the given path"""
    try:
        entries = os.scandir(path)
        return [entry.name for entry in entries]
    except FileNotFoundError:
        flash(f"The path '{path}' does not exist.", "error")
        return []

def rename_file(old_name, new_name):
    """Rename a file or directory"""
    try:
        os.rename(old_name, new_name)
        flash(f"Renamed '{old_name}' to '{new_name}'.", "success")
    except FileNotFoundError:
        flash(f"File or directory '{old_name}' not found.", "error")

def delete_file(file_path):
    """Delete a file"""
    try:
        os.remove(file_path)
        flash(f"File '{file_path}' deleted successfully.", "success")
    except FileNotFoundError:
        flash(f"File '{file_path}' not found.", "error")

def delete_directory(directory_path):
    """Delete a directory and all its contents"""
    try:
        shutil.rmtree(directory_path)
        flash(f"Directory '{directory_path}' deleted successfully.", "success")
    except FileNotFoundError:
        flash(f"Directory '{directory_path}' not found.", "error")

def move_file(source, destination):
    """Move a file from source to destination"""
    try:
        shutil.move(source, destination)
        flash(f"Moved '{source}' to '{destination}'.", "success")
    except FileNotFoundError:
        flash(f"File '{source}' or destination '{destination}' not found.", "error")

# Routes for the website
@app.route('/')
def index():
    files_and_dirs = list_directory() 
    return render_template('index.html', files=files_and_dirs)

@app.route('/create-directory', methods=['POST'])
def handle_create_directory():
    dir_name = request.form.get('directory_name')
    create_directory(dir_name)
    return redirect(url_for('index'))

@app.route('/create-file', methods=['POST'])
def handle_create_file():
    file_path = request.form.get('file_path')
    content = request.form.get('content')
    create_file(file_path, content)
    return redirect(url_for('index'))

@app.route('/rename', methods=['POST'])
def handle_rename():
    old_name = request.form.get('old_name')
    new_name = request.form.get('new_name')
    rename_file(old_name, new_name)
    return redirect(url_for('index'))

@app.route('/delete-file', methods=['POST'])
def handle_delete_file():
    file_path = request.form.get('file_path')
    delete_file(file_path)
    return redirect(url_for('index'))

@app.route('/delete-directory', methods=['POST'])
def handle_delete_directory():
    directory_path = request.form.get('directory_path')
    delete_directory(directory_path)
    return redirect(url_for('index'))

@app.route('/move-file', methods=['POST'])
def handle_move_file():
    source = request.form.get('source')
    destination = request.form.get('destination')
    move_file(source, destination)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
