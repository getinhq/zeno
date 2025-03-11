from .tool_registry import ToolRegistry
from .base import ZenoBaseTool
import bpy

class ZENO_MT_ToolsMenu(bpy.types.Menu):
    """Dynamic menu for all Zeno tools."""
    bl_idname = "ZENO_MT_tools_menu"
    bl_label = "Zeno Tools"
    
    def draw(self, context):
        """Draw the menu with all registered tools."""
        layout = self.layout
        layout.operator("zeno.reload_tools", icon='FILE_REFRESH')
        layout.separator()
        
        # Dynamically add all registered tools
        for tool in ToolRegistry.get_all_tools():
            layout.operator(tool.bl_idname, text=tool.bl_label)

def register():
    """Register all Zeno components."""
    # Discover and load all tools
    ToolRegistry.discover_tools()
    
    # Register the menu
    bpy.utils.register_class(ZENO_MT_ToolsMenu)
    
    # Register all tools
    ToolRegistry.register_all()
    
    # Add menu to the interface
    bpy.types.TOPBAR_MT_editor_menus.append(add_menu_to_topbar)

def unregister():
    """Unregister all Zeno components."""
    # Remove menu from interface
    bpy.types.TOPBAR_MT_editor_menus.remove(add_menu_to_topbar)
    
    # Unregister the menu
    bpy.utils.unregister_class(ZENO_MT_ToolsMenu)
    
    # Unregister all tools
    ToolRegistry.unregister_all()

def add_menu_to_topbar(self, context):
    """Add the Zeno menu to the top bar."""
    layout = self.layout
    layout.separator()
    layout.menu(ZENO_MT_ToolsMenu.bl_idname)