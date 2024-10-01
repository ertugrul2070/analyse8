import os
import shutil
import zipfile
from datetime import datetime

def create_backup():
    try:
        # Create a backups directory if it doesn't exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_path = os.path.join(script_dir, 'backups')
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        # Get the current date and time
        current_date_time = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Define the backup file name
        backup_filename = f'backup_{current_date_time}.zip'
        backup_filepath = os.path.join(backup_path, backup_filename)

        # Create a zip file and add the files
        with zipfile.ZipFile(backup_filepath, 'w') as backup_zip:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, 'UniqueMeal.db')
            backup_zip.write(db_path)
            log_path = os.path.join(script_dir, 'encrypted_logs.log')
            backup_zip.write(log_path)

        print(f'Backup created: {backup_filename}')
        input("press ENTER to go back")
        return True, backup_filename
    except Exception as e:
        return  False, ""

def list_backups():
    # List all the backup files in the backups directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_path = os.path.join(script_dir, 'backups')
    if not os.path.exists(backup_path):
        print('No backups found.')
        return []

    backups = [f for f in os.listdir(backup_path) if f.endswith('.zip')]
    i = 0
    print('No. | filename | date of backup')
    print('##############################')
    for backup in backups:
        date_str = backup[len('backup_'):-len('.zip')]
        date_time = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
        print(f'{i} - {backup} - {date_time.strftime("%Y-%m-%d %H:%M:%S")}')
        i = i + 1
    
    selectedBackup = input("Enter the number of the backup you want to choose (leave empty to cancel backup): ")
    if selectedBackup != '':
        if input(f"are you sure you want to load backup {backups[int(selectedBackup)]} (y/n): ") == 'y':
            return backups[int(selectedBackup)]
    else:
        input("Invalid input, press ENTER to go back")
    return

def restore_backup():
    try:
        backup_filename = list_backups()
        # Ensure the backup file exists
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_path = os.path.join(script_dir, 'backups')
        backup_filepath = os.path.join(backup_path, backup_filename)
        if not os.path.exists(backup_filepath):
            print(f'Backup file {backup_filename} does not exist.')
            return False, ""
        # Extract the backup file contents to the src directory
        src_path = script_dir  # Assuming you want to extract to the same directory as the script
        with zipfile.ZipFile(backup_filepath, 'r') as backup_zip:
            # Iterate over the zip file contents
            for member in backup_zip.namelist():
                member_path = os.path.join(src_path, os.path.relpath(member, start=os.path.commonpath(backup_zip.namelist())))
                os.makedirs(os.path.dirname(member_path), exist_ok=True)
                if member.endswith('/'):
                    os.makedirs(member_path, exist_ok=True)
                else:
                    # File
                    with backup_zip.open(member) as source, open(member_path, 'wb') as target:
                        target.write(source.read())

        print(f'Backup {backup_filename} restored successfully.')
        input("press ENTER to go back")
        return True, backup_filename
    except Exception as e:
        return  False, ""

# if __name__ == '__main__':
    # Create a backup
    # create_backup()

    # List all backups
    # list_backups()

    # Restore a specific backup
    # restore_backup()
