from ..base import ZenoBaseTool

class ZENO_OT_Tool1(ZenoBaseTool):
    """First example tool demonstrating the Zeno toolkit."""
    bl_idname = "zeno.cubmesh"
    bl_label = "Create Cube Mesh ( Test Tool )"
    bl_description = "Performs Creation of a Cube Mesh"

    def execute(self, context):
        """Execute Tool 1 operation."""
        import bpy
        
        # Create a new cube mesh
        mesh = bpy.data.meshes.new(name="Cube")
        obj = bpy.data.objects.new("Cube", mesh)
        
        # Link the object to the active collection
        bpy.context.collection.objects.link(obj)
        
        # Create cube vertices
        verts = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]
        
        # Create cube faces
        faces = [
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 7, 3),
            (1, 5, 6, 2), (0, 1, 5, 4), (3, 2, 6, 7)
        ]
        
        # Update mesh with new data
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        
        # Select the new object and make it active
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        return {'FINISHED'}