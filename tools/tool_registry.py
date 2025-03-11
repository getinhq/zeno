import bpy
import importlib
import pkgutil
from typing import List, Type
from . import operators
from .base import ZenoBaseTool

class ToolRegistry:
    """Manages registration and loading of all Zeno tools."""
    
    _tools: List[Type[ZenoBaseTool]] = []
    
    @classmethod
    def register_tool(cls, tool_class: Type[ZenoBaseTool]):
        """Register a new tool class."""
        if tool_class not in cls._tools:
            cls._tools.append(tool_class)
    
    @classmethod
    def discover_tools(cls):
        """Automatically discover and load all tool modules."""
        cls._tools.clear()
        
        # Iterate through all modules in the operators package
        for _, name, _ in pkgutil.iter_modules(operators.__path__):
            # Import or reload the module
            if f"{operators.__name__}.{name}" in importlib.sys.modules:
                module = importlib.reload(importlib.sys.modules[f"{operators.__name__}.{name}"])
            else:
                module = importlib.import_module(f"{operators.__name__}.{name}")
            
            # Register any ZenoBaseTool subclasses found in the module
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (isinstance(item, type) and 
                    issubclass(item, ZenoBaseTool) and 
                    item != ZenoBaseTool):
                    cls.register_tool(item)
    
    @classmethod
    def register_all(cls):
        """Register all tools with Blender."""
        for tool in cls._tools:
            bpy.utils.register_class(tool)
    
    @classmethod
    def unregister_all(cls):
        """Unregister all tools from Blender."""
        for tool in reversed(cls._tools):
            bpy.utils.unregister_class(tool)
    
    @classmethod
    def get_all_tools(cls) -> List[Type[ZenoBaseTool]]:
        """Return list of all registered tools."""
        return cls._tools.copy()