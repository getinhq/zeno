import subprocess
import os
from pathlib import Path
from load_env import load_env_file

# Load environment variables from .env file
load_env_file()

# Now you can access the environment variables
BLENDER_EXECUTABLE = os.getenv('ZENO_BLENDER_PATH')
CUSTOM_ENV_PATH = os.getenv('ZENO_ENV_PATH')
ZENO_TOOLS_PATH = os.getenv('ZENO_TOOLS_PATH')
ZENO_TOOLS_SCRIPT = os.getenv('ZENO_TOOLS_SCRIPT')
ZENO_PROD_PATH = os.getenv('ZENO_PROD_PATH')
# Add validation to ensure required environment variables are set
def validate_env_vars():
    required_vars = {
        'ZENO_BLENDER_PATH': BLENDER_EXECUTABLE,
        'ZENO_ENV_PATH': CUSTOM_ENV_PATH,
        'ZENO_TOOLS_PATH': ZENO_TOOLS_PATH,
        'ZENO_TOOLS_SCRIPT': ZENO_TOOLS_SCRIPT
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            "Please set these variables in the .env file."
        )

# ------------------------------------------------------------------------
# Build Blender Command
# ------------------------------------------------------------------------
def launch_blender():
    # Create a temporary Python script that will be executed by Blender
    temp_script = """
import sys
import os
import bpy

# Add paths
sys.path.append(r'{}')
sys.path.append(r'{}')
sys.path.append(r'{}')

# Execute the setup script
with open(r'{}', 'r') as file:
    exec(file.read())
""".format(ZENO_PROD_PATH, CUSTOM_ENV_PATH, ZENO_TOOLS_PATH, ZENO_TOOLS_SCRIPT)

    # Write the temporary script
    temp_script_path = os.path.join(os.path.dirname(__file__), "temp_startup.py")
    with open(temp_script_path, "w") as f:
        f.write(temp_script)

    # Launch Blender with the temporary script
    command = [
        BLENDER_EXECUTABLE,
        "--python",
        temp_script_path
    ]

    try:
        subprocess.run(command)
    finally:
        # Clean up the temporary script
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)

if __name__ == "__main__":
    launch_blender()