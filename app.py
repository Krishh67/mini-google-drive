import os
import uuid
from flask import Flask, render_template, request, send_from_directory, url_for, redirect

app = Flask(__name__)

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists on startup
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# A simple dictionary to map unique IDs to filenames.
files_db = {}

@app.route('/', methods=['GET'])
def index():
    """Renders the main Drive page."""
    # Convert files_db dict into a list of dictionaries for easier templating,
    # reversing it so the newest files appear first
    files_list = [{'id': k, 'filename': v} for k, v in reversed(list(files_db.items()))]
    
    return render_template('index.html', files=files_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles the file upload directly from the + New button."""
    if 'file' not in request.files:
        return redirect(url_for('index'))
        
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
        
    if file:
        filename = file.filename
        
        try:
            # Save the file
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            
            # Generate a unique ID and store it
            file_id = str(uuid.uuid4())
            files_db[file_id] = filename
            
            # Redirect back to the UI which will now refresh and show the new file
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred during upload: {str(e)}", 500

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """Serves the file associated with the unique ID."""
    filename = files_db.get(file_id)
    if not filename:
        return "File not found.", 404
        
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return f"An error occurred during download: {str(e)}", 500

@app.route('/delete/<file_id>', methods=['POST'])
def delete_file(file_id):
    """Deletes the file associated with the unique ID."""
    filename = files_db.get(file_id)
    if not filename:
        return "File not found.", 404
        
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        del files_db[file_id]
        return redirect(url_for('index'))
    except Exception as e:
        return f"An error occurred during deletion: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
