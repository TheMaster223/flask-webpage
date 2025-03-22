#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

SAVE_PATH = 'saved_data.txt'

# Ensure the file exists before running the app
if not os.path.exists(SAVE_PATH):
    try:
        with open(SAVE_PATH, 'w') as f:
            pass  # Create an empty file if it doesn't exist
    except PermissionError:
        print(f"Permission denied: Cannot create {SAVE_PATH}. Please check your permissions.")
        exit(1)

@app.route('/')
def index():
    try:
        with open(SAVE_PATH, 'a+') as f:
            f.seek(0)  # Move the file pointer to the start
            saved_data = f.readlines()
    except PermissionError:
        return "Permission denied: Cannot read or write to the file. Please check your permissions.", 500
    return render_template('index.html', saved_data=saved_data)

@app.route('/save', methods=['POST'])
def save_data():
    user_input = request.form['user_input']
    
    try:
        with open(SAVE_PATH, 'a') as f:
            f.write(user_input + '\n')
    except PermissionError:
        return "Permission denied: Cannot write to the file. Please check your permissions.", 500
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
