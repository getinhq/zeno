
import sys
import os
import bpy

# Add paths
sys.path.append(r'/Users/zeno/Desktop/local-git/zeno')
sys.path.append(r'/Users/zeno/Desktop/local-git/zeno/zeno-env/lib/python3.9/site-packages')
sys.path.append(r'/Users/zeno/Desktop/local-git/zeno/tools')

# Execute the setup script
with open(r'/Users/zeno/Desktop/local-git/zeno/zeno_tools_setup.py', 'r') as file:
    exec(file.read())
