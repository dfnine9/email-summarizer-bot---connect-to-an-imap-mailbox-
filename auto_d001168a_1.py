"""
backup_config.py

This script creates a skill file that defines parameters for a backup script.
It includes the source directory, backup directory, file types to include, and
backup frequency. The script also handles potential errors and prints the results
to standard output.
"""

import json
import os

def create_backup_config(source_dir, backup_dir, file_types, backup_frequency):
    try:
        config = {
            "source_directory": source_dir,
            "backup_directory": backup_dir,
            "file_types": file_types,
            "backup_frequency": backup_frequency
        }

        config_file_path = os.path.join(backup_dir, "backup_config.json")
        
        with open(config_file_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)

        print(f"Backup configuration successfully created at: {config_file_path}")
        print(json.dumps(config, indent=4))

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Example parameters
    source_directory = "/path/to/source"
    backup_directory = "/path/to/backup"
    file_types_to_include = ["*.txt", "*.jpg"]
    backup_frequency = "daily"

    create_backup_config(source_directory, backup_directory, file_types_to_include, backup_frequency)