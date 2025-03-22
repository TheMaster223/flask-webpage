import os
import base64
import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get GitHub details from environment variables
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')  # Set this in .env file
REPO_NAME = os.getenv('REPO_NAME')  # Set this in .env file
FILE_PATH = 'saved_data.txt'  # Path to the file in your repository
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # GitHub Token from .env file

# GitHub API URL to interact with files
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"

# Function to get the current contents of the saved_data.txt file from GitHub
def get_saved_data():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(GITHUB_API_URL, headers=headers)
    
    if response.status_code == 200:
        content = response.json()['content']
        decoded_content = base64.b64decode(content).decode('utf-8')
        return decoded_content
    else:
        return "Error: Could not fetch data."

# Function to save new data to the saved_data.txt file on GitHub
def save_data_to_github(data):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
    # Get the current contents of the file and append new data
    current_content = get_saved_data()
    new_content = current_content + "\n" + data
    
    # Encode the new content to base64
    encoded_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')
    
    # Get the current sha of the file (required for updating the file)
    sha = get_file_sha()
    
    if sha is None:
        return "Error: File not found or cannot fetch sha."
    
    payload = {
        'message': 'Added new data',
        'content': encoded_content,
        'sha': sha
    }
    
    response = requests.put(GITHUB_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return "Data saved successfully!"
    else:
        return f"Error: {response.json()['message']}"

# Function to get the sha of the file (needed for updating)
def get_file_sha():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(GITHUB_API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()['sha']
    else:
        return None

# Route for the homepage
@app.route('/')
def index():
    saved_data = get_saved_data()  # Get the current data from GitHub
    return render_template('index.html', saved_data=saved_data)

# Route to handle the form submission
@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        new_data = request.form['data']  # Get the data from the form
        save_message = save_data_to_github(new_data)  # Save the new data to GitHub
        return redirect(url_for('index'))  # Redirect back to the homepage

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
