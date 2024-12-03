import os
import zipfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import tempfile
import time
import shutil

app = Flask(__name__)

# Define allowed extensions for images and zip files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'zip'}

# Maximum file size (1GB = 1,073,741,824 bytes)
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB in bytes


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_image(image_path, output_path, resize_ratio):
    """Resize an image by a given ratio."""
    with Image.open(image_path) as image:
        # Calculate new size
        new_width = int(image.width * resize_ratio)
        new_height = int(image.height * resize_ratio)
        new_size = (new_width, new_height)

        # Resize the image
        resized_image = image.resize(new_size)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the resized image
        resized_image.save(output_path)


def zip_folder(files, zip_name):
    """Zip the list of files into a single zip file."""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            zip_file.write(file, os.path.basename(file))  # Store file name only, not full path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    # Check if the file is too large
    if request.content_length > MAX_FILE_SIZE:
        return 'File is too large. The maximum allowed file size is 1GB.'

    resize_ratio = float(request.form['resize_ratio'])

    # Ensure the file is allowed
    if file.filename == '' or not allowed_file(file.filename):
        return 'Invalid file format. Please upload an image or a zip file.'

    # Create a unique timestamped folder for the upload
    timestamp = int(time.time())
    temp_folder = os.path.join(tempfile.gettempdir(), f"upload_{timestamp}")
    os.makedirs(temp_folder, exist_ok=True)

    resized_files = []

    # If it's a zip file, extract it into the timestamped folder
    if file.filename.endswith('.zip'):
        zip_filename = os.path.join(temp_folder, 'uploaded.zip')
        file.save(zip_filename)

        # Extract the contents of the zip file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)

        # Process the extracted files (only images, skip non-image files)
        for root, dirs, files in os.walk(temp_folder):
            for extracted_file in files:
                extracted_file_path = os.path.join(root, extracted_file)
                if allowed_file(extracted_file):
                    resized_file_path = os.path.join(temp_folder, f"resized_{extracted_file}")
                    try:
                        # Resize the image
                        resize_image(extracted_file_path, resized_file_path, resize_ratio)
                        resized_files.append(resized_file_path)
                    except Exception as e:
                        print(f"Error resizing {extracted_file_path}: {e}")
    else:
        # If it's a single image, save it directly
        image_path = os.path.join(temp_folder, secure_filename(file.filename))
        file.save(image_path)
        resized_file_path = os.path.join(temp_folder, f"resized_{file.filename}")
        resize_image(image_path, resized_file_path, resize_ratio)
        resized_files.append(resized_file_path)

    # Create a zip file of the resized images only from this specific upload
    zip_output = os.path.join(temp_folder, 'resized_images.zip')
    zip_folder(resized_files, zip_output)

    # Return the zip file to the user for download
    return send_file(zip_output, as_attachment=True, download_name="resized_images.zip")


if __name__ == '__main__':
    app.run(debug=True)
