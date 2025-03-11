import bpy
from typing import Dict, Any

class ZenoBaseTool(bpy.types.Operator):
    """Base class for all Zeno tools."""
    bl_idname = "zeno.undefined"
    bl_label = "Undefined"
    bl_description = "Base class for Zeno tools"

    @classmethod
    def get_tool_id(cls) -> str:
        """Returns the unique identifier for this tool."""
        return cls.bl_idname.split('.')[1]

    def execute(self, context) -> Dict[str, Any]:
        """Default execute method."""
        raise NotImplementedError("Tool must implement execute method")