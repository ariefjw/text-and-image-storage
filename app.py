import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file
from werkzeug.utils import secure_filename
import json

# Try to import PIL, but don't fail if it's not available
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configure upload folders
TEXT_FOLDER = '/tmp/texts'  # Using /tmp for Vercel
IMAGE_FOLDER = '/tmp/uploads'  # Using /tmp for Vercel
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create necessary directories
for folder in [TEXT_FOLDER, IMAGE_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_text_files():
    texts = []
    for filename in os.listdir(TEXT_FOLDER):
        if filename.endswith('.txt'):
            with open(os.path.join(TEXT_FOLDER, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                texts.append({
                    'id': filename.replace('.txt', ''),
                    'content': content,
                    'date': datetime.fromtimestamp(os.path.getctime(os.path.join(TEXT_FOLDER, filename))).strftime('%Y-%m-%d %H:%M:%S')
                })
    return sorted(texts, key=lambda x: x['date'], reverse=True)

def get_image_files():
    images = []
    for filename in os.listdir(IMAGE_FOLDER):
        if any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            images.append({
                'id': filename.split('.')[0],
                'filename': filename,
                'date': datetime.fromtimestamp(os.path.getctime(os.path.join(IMAGE_FOLDER, filename))).strftime('%Y-%m-%d %H:%M:%S')
            })
    return sorted(images, key=lambda x: x['date'], reverse=True)

@app.route('/')
def index():
    texts = get_text_files()
    images = get_image_files()
    return render_template('index.html', texts=texts, images=images)

@app.route('/add_text', methods=['POST'])
def add_text():
    text = request.form.get('text')
    if text:
        # Generate unique filename
        filename = f"{uuid.uuid4()}.txt"
        filepath = os.path.join(TEXT_FOLDER, filename)
        
        # Save text to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        flash('Text added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No image selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['image']
    if file.filename == '':
        flash('No image selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename while preserving extension
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(app.config['IMAGE_FOLDER'], filename)
            
            # Save the file
            file.save(filepath)
            
            # If Pillow is available, try to verify the image
            if PILLOW_AVAILABLE:
                try:
                    with Image.open(filepath) as img:
                        img.verify()
                except Exception as e:
                    os.remove(filepath)
                    flash('Invalid image file', 'error')
                    return redirect(url_for('index'))
            
            flash('Image uploaded successfully!', 'success')
        except Exception as e:
            flash(f'Error uploading image: {str(e)}', 'error')
    else:
        flash('Invalid file type', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_text/<text_id>')
def delete_text(text_id):
    filename = f"{text_id}.txt"
    filepath = os.path.join(TEXT_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash('Text deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_image/<image_id>')
def delete_image(image_id):
    # Find the image file with the matching ID
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.startswith(image_id):
            filepath = os.path.join(IMAGE_FOLDER, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                flash('Image deleted successfully!', 'success')
            break
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['IMAGE_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        flash('Error downloading file', 'error')
        return redirect(url_for('index'))

# For local development
if __name__ == '__main__':
    app.run(debug=True) 