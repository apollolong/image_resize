import os
import time
import shutil

# Define the path to the temp directory where the files are stored
TEMP_DIR = os.path.join(os.getenv('TEMP'), "upload_*")  # Using a pattern to match temp folders

# Define the time threshold (2 hours)
TIME_THRESHOLD = 2 * 60 * 60  # 2 hours in seconds

def delete_old_files():
    """Delete files older than 2 hours in the temporary folder."""
    # Get the current time
    current_time = time.time()

    # Loop through all files and directories in the temp folder
    for folder in os.listdir(os.getenv('TEMP')):
        folder_path = os.path.join(os.getenv('TEMP'), folder)

        if os.path.isdir(folder_path) and folder.startswith("upload_"):
            # Loop through the files inside the folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                # Check if the file is older than the threshold
                if os.path.isfile(file_path):
                    file_mod_time = os.path.getmtime(file_path)
                    if current_time - file_mod_time > TIME_THRESHOLD:
                        print(f"Deleting old file: {file_path}")
                        os.remove(file_path)  # Delete the file

            # After deleting files, check if the folder is empty
            if not os.listdir(folder_path):
                print(f"Deleting empty folder: {folder_path}")
                shutil.rmtree(folder_path)  # Remove the empty folder

if __name__ == "__main__":
    delete_old_files()
