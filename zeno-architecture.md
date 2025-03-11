# Zeno Tools Architecture

## Overview
The Zeno tools system is a modular Blender addon architecture that provides a framework for creating and managing tools in Blender. The system consists of three main components:

1. Setup and Menu Creation (`zeno_tools_setup.py`)
2. Base Tool Class (`base.py`)
3. Tool Registry (`tool_registry.py`)

## Component Details

### 1. Setup and Menu Creation
`zeno_tools_setup.py` handles:
- Python path setup for custom environments
- Menu creation in Blender's interface
- Tool reloading functionality
- Registration/unregistration of the system

Key components:
```

### 2. Base Tool Class
`base.py` provides the foundation for all Zeno tools:
- Defines common properties and methods
- Inherits from `bpy.types.Operator`
- Forces implementation of required methods

Example of creating a new tool:
```

### 3. Tool Registry
`tool_registry.py` manages tool discovery and registration:
- Automatically discovers tools in the `operators` package
- Handles registration/unregistration with Blender
- Maintains list of available tools

## Workflow

1. **Tool Loading Process**:
   ```mermaid
   graph TD
       A[Blender Starts] --> B[zeno_tools_setup.py loads]
       B --> C[ToolRegistry.discover_tools()]
       C --> D[Scan operators package]
       D --> E[Register found tools]
       E --> F[Create menu entries]
   ```

2. **Tool Creation Workflow**:
   - Create new tool file in `operators` directory
   - Inherit from `ZenoBaseTool`
   - Tool automatically discovered and registered

3. **Menu Integration**:
   - Tools appear in "Zeno Tools" menu
   - Reload button available for development
   - Menu accessible from Blender's top bar

## Tool Registration Flow

1. **Discovery**:
   - `ToolRegistry.discover_tools()` scans the `operators` package
   - Finds all classes inheriting from `ZenoBaseTool`
   - Adds them to internal registry

2. **Registration**:
   - `ToolRegistry.register_all()` registers tools with Blender
   - Each tool becomes available as an operator
   - Menu updated with new tools

3. **Usage**:
   - Tools accessible via menu or Python API
   - Each tool execution calls its `execute()` method
   - Results reported back to Blender

## Development Tips

1. **Creating New Tools**:
   ```python
   # operators/my_tool.py
   from tools.base import ZenoBaseTool
   
   class MyTool(ZenoBaseTool):
       bl_idname = "zeno.my_tool"
       bl_label = "My Tool"
       
       def execute(self, context):
           # Implementation
           return {'FINISHED'}
   ```

2. **Reloading During Development**:
   - Use "Reload Zeno Tools" from menu
   - Updates all tools without restarting Blender

3. **Best Practices**:
   - Keep tools modular and focused
   - Use descriptive bl_idname and bl_label
   - Implement proper error handling
   - Document tool functionality

## Error Handling

The system includes several layers of error handling:
- Import error catching
- Tool registration verification
- Reload operation safety checks

This ensures stability while allowing for development flexibility.