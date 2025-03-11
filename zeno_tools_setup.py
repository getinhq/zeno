import bpy
import sys
import os
from pathlib import Path
from load_env import load_env_file

# Load environment variables from .env file
load_env_file()

# Add the parent directory of zeno_tools_setup.py to Python path
SCRIPT_DIR = Path(__file__).parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

# Add Custom Python Environment from environment variable
CUSTOM_ENV_PATH = os.getenv('ZENO_ENV_PATH')
if CUSTOM_ENV_PATH and CUSTOM_ENV_PATH not in sys.path:
    sys.path.append(CUSTOM_ENV_PATH)

# Import the tools package
try:
    import tools
    from tools import register, unregister
except ImportError as e:
    print(f"Error importing Zeno tools package: {e}")
    print(f"Current sys.path: {sys.path}")

# ------------------------------------------------------------------------
# Define the "Zeno Tools" Menu
# ------------------------------------------------------------------------
def reload_zeno_tools():
    """Reloads all Zeno tool modules and re-registers them in Blender.
    
    This function unregisters existing classes, reloads all modules prefixed with 'tools.',
    and re-registers everything to ensure the latest version of the tools are loaded.
    """
    try:
        unregister()
    except:
        pass
    
    for module in list(sys.modules.keys()):
        if module.startswith('tools.'):
            importlib.reload(sys.modules[module])
    
    register()
    
class ZENO_OT_ReloadTools(bpy.types.Operator):
    """Operator to reload all Zeno tools and their configurations."""
    bl_idname = "zeno.reload_tools"
    bl_label = "Reload Zeno Tools"
    
    def execute(self, context):
        """Reload all tools and their configurations."""
        try:
            # Unregister everything
            unregister()
            
            # Reload the main tools package and all submodules
            import importlib
            importlib.reload(tools)
            
            # Re-register everything
            register()
            
            self.report({'INFO'}, "Zeno Tools Reloaded Successfully!")
        except Exception as e:
            self.report({'ERROR'}, f"Error reloading tools: {e}")
        
        return {'FINISHED'}

class ZENO_MT_ToolsMenu(bpy.types.Menu):
    """Menu for Zeno tools in the Blender interface."""
    bl_idname = "ZENO_MT_tools_menu"
    bl_label = "Zeno"
    
    def draw(self, context):
        """Draw the menu layout.
        
        Args:
            context: Blender context
        """
        layout = self.layout
        layout.operator(ZENO_OT_ReloadTools.bl_idname, icon='FILE_REFRESH')
        layout.separator()
        layout.operator("zeno.tool1", text="Tool 1")
        layout.operator("zeno.tool2", text="Tool 2")

def add_menu_to_topbar(self, context):
    """Adds the Zeno tools menu to Blender's top bar.
    
    Args:
        self: Menu class instance
        context: Blender context
    """
    layout = self.layout
    layout.separator()
    layout.menu(ZENO_MT_ToolsMenu.bl_idname)

# ------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------
classes = [ZENO_MT_ToolsMenu, ZENO_OT_ReloadTools]

def register():
    """Register the reload operator and initialize all tools."""
    # Register the reload operator
    bpy.utils.register_class(ZENO_OT_ReloadTools)
    
    # Register all tools and menus
    tools.register()

def unregister():
    """Unregister everything."""
    # Unregister all tools and menus
    tools.unregister()
    
    # Unregister the reload operator
    bpy.utils.unregister_class(ZENO_OT_ReloadTools)

if __name__ == "__main__":
    register()