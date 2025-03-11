import bpy
from ..base import ZenoBaseTool


def create_armature(name, location=(0, 0, 0)):
    # Create a new armature object
    bpy.ops.object.armature_add(enter_editmode=True, location=location)
    armature = bpy.context.object
    armature.name = name
    
    # Switch to Edit Mode to add bones
    bpy.ops.object.mode_set(mode='EDIT')
    return armature

def create_bone(armature, name, head, tail, parent_bone=None):
    # Create a new bone
    bone = armature.data.edit_bones.new(name)
    bone.head = head
    bone.tail = tail
    if parent_bone:
        bone.parent = armature.data.edit_bones[parent_bone]
    return bone

class ZENO_OT_CreateHumanRig(ZenoBaseTool):
    """Creates a basic human armature rig."""
    bl_idname = "zeno.create_human_rig"
    bl_label = "Create Human Rig"
    bl_description = "Creates a basic human armature with standard bone structure"

    def create_armature(self, name, location=(0, 0, 0)):
        # Create a new armature object
        bpy.ops.object.armature_add(enter_editmode=True, location=location)
        armature = bpy.context.object
        armature.name = name
        
        # Switch to Edit Mode to add bones
        bpy.ops.object.mode_set(mode='EDIT')
        return armature

    def execute(self, context):
        """Execute the human rig creation."""
        # Clear existing armatures
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='ARMATURE')
        bpy.ops.object.delete()
        
        # Create the main armature
        armature = self.create_armature("Human_Rig", location=(0, 0, 0))
        
        # Create spine
        create_bone(armature, 'spine_base', (0, 0, 0), (0, 0, 1))
        create_bone(armature, 'spine_mid', (0, 0, 1), (0, 0, 2), parent_bone='spine_base')
        create_bone(armature, 'spine_top', (0, 0, 2), (0, 0, 3), parent_bone='spine_mid')
        
        # Create arms
        # Left arm
        create_bone(armature, 'shoulder.L', (0, 0.2, 2.5), (0, 0.5, 2.5), parent_bone='spine_top')
        create_bone(armature, 'upper_arm.L', (0, 0.5, 2.5), (0, 0.8, 2.5), parent_bone='shoulder.L')
        create_bone(armature, 'lower_arm.L', (0, 0.8, 2.5), (0, 1.1, 2.5), parent_bone='upper_arm.L')

        # Right arm
        create_bone(armature, 'shoulder.R', (0, -0.2, 2.5), (0, -0.5, 2.5), parent_bone='spine_top')
        create_bone(armature, 'upper_arm.R', (0, -0.5, 2.5), (0, -0.8, 2.5), parent_bone='shoulder.R')
        create_bone(armature, 'lower_arm.R', (0, -0.8, 2.5), (0, -1.1, 2.5), parent_bone='upper_arm.R')
        
        # Create legs
        # Left leg
        create_bone(armature, 'hip.L', (0, 0.2, 0), (0, 0.2, -1), parent_bone='spine_base')
        create_bone(armature, 'thigh.L', (0, 0.2, -1), (0, 0.2, -2), parent_bone='hip.L')
        create_bone(armature, 'shin.L', (0, 0.2, -2), (0, 0.2, -3), parent_bone='thigh.L')

        # Right leg
        create_bone(armature, 'hip.R', (0, -0.2, 0), (0, -0.2, -1), parent_bone='spine_base')
        create_bone(armature, 'thigh.R', (0, -0.2, -1), (0, -0.2, -2), parent_bone='hip.R')
        create_bone(armature, 'shin.R', (0, -0.2, -2), (0, -0.2, -3), parent_bone='thigh.R')
        
        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        return {'FINISHED'}

# create_human_rig()

print("Human rig created!")

# To use this script, paste it into Blender's scripting editor and hit Run!
# Make sure your 3D cursor is at the origin (0,0,0) for best results.
