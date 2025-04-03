import os
import shutil
import re
import glob
from pathlib import Path

def force_clean():
    """Forcibly remove the website directory (preserving .git)"""
    print("Starting forceful cleanup...")
    
    # Backup .git directory if it exists inside website
    if os.path.exists('website/.git'):
        print("Backing up .git directory...")
        if os.path.exists('.git_backup'):
            shutil.rmtree('.git_backup')
        shutil.copytree('website/.git', '.git_backup')
    
    # Delete the website directory if it exists
    if os.path.exists('website'):
        print("Deleting website directory...")
        try:
            shutil.rmtree('website')
            print("Website directory deleted successfully.")
        except Exception as e:
            print(f"Error deleting website directory: {e}")
            # Try a more granular approach
            for root, dirs, files in os.walk('website', topdown=True):
                # Skip .git directory
                if '.git' in dirs:
                    dirs.remove('.git')
                
                # Delete files first
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Could not delete {file_path}: {e}")
            
            # Then try to remove dirs
            for root, dirs, files in os.walk('website', topdown=False):
                # Skip .git directory
                if '.git' in dirs:
                    dirs.remove('.git')
                
                for dir_name in dirs:
                    try:
                        dir_path = os.path.join(root, dir_name)
                        os.rmdir(dir_path)
                    except Exception as e:
                        print(f"Could not delete {dir_path}: {e}")
    
    # Create fresh website directory
    print("Creating fresh website directory...")
    os.makedirs('website', exist_ok=True)
    
    # Restore .git if we backed it up
    if os.path.exists('.git_backup'):
        print("Restoring .git directory...")
        shutil.copytree('.git_backup', 'website/.git')
        shutil.rmtree('.git_backup')
    
    print("Forceful cleanup completed.")

def main():
    force_clean()
    print("Now you can run your restructuring script on a clean directory.")

if __name__ == "__main__":
    main() 