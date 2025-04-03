import os
import subprocess

def setup_github_repo():
    """
    Sets up git repository and pushes code to GitHub
    """
    # Initialize git repository
    subprocess.run(['git', 'init'], check=True)
    
    # Create .gitignore file
    with open('.gitignore', 'w') as f:
        f.write('''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
''')
    
    # Add all files
    subprocess.run(['git', 'add', '.'], check=True)
    
    # Commit changes
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    # Remove existing remote if it exists
    try:
        subprocess.run(['git', 'remote', 'remove', 'origin'], check=True)
    except subprocess.CalledProcessError:
        pass  # Remote doesn't exist, which is fine
    
    # Add remote repository
    subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/GaragesWirral/selfstoragedirectory.git'], check=True)
    
    # Push to master branch
    subprocess.run(['git', 'push', '-u', 'origin', 'master'], check=True)
    
    print("Repository setup and code push completed successfully!")

if __name__ == "__main__":
    setup_github_repo() 