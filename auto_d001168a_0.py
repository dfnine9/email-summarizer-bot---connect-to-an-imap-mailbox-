"""
This script identifies files in a specified directory and creates a timestamped backup
in a different location. It includes error handling to manage potential issues with file
operations and prints the results to stdout.
"""

import os
import shutil
import datetime

def backup_files(source_dir, backup_dir):
    """Backs up files from source_dir to backup_dir with a timestamp."""
    try:
        # Ensure the source directory exists
        if not os.path.isdir(source_dir):
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")
        
        # Create a timestamp for the backup
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(backup_dir, f"backup_{timestamp}")
        
        # Create the backup directory
        os.makedirs(backup_folder, exist_ok=True)

        # Iterate through files in the source directory
        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            if os.path.isfile(source_file):
                # Copy the file to the backup directory
                shutil.copy2(source_file, backup_folder)
                print(f"Backed up '{filename}' to '{backup_folder}'")
        
        print("Backup completed successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    source_directory = input("Enter the source directory: ")
    backup_directory = input("Enter the backup directory: ")
    backup_files(source_directory, backup_directory)