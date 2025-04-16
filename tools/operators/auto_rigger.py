import bpy
from mathutils import Vector
from ..base import ZenoBaseTool

class AutoRiggerTool:
    """Utility class for Auto Rigger functionality"""
    @staticmethod
    def create_armature(name, location=(0, 0, 0)):
        """Create a new armature object"""
        bpy.ops.object.armature_add(enter_editmode=True, location=location)
        armature = bpy.context.object
        armature.name = name
        return armature

    @staticmethod
    def create_bone(armature, name, head, tail, parent_bone=None):
        """Create a new bone in the armature"""
        bone = armature.data.edit_bones.new(name)
        bone.head = head
        bone.tail = tail
        if parent_bone and parent_bone in armature.data.edit_bones:
            bone.parent = armature.data.edit_bones[parent_bone]
        return bone

    @staticmethod
    def create_guide(name, location, size=0.1):
        """Create a guide object at specified location"""
        bpy.ops.mesh.primitive_cube_add(size=size, location=location)
        guide = bpy.context.active_object
        guide.name = name
        
        # Add custom properties
        guide["bendy_joints"] = 2
        guide["stretchable"] = False
        
        return guide

class AutoRiggerProperties(bpy.types.PropertyGroup):
    """Properties for the Auto Rigger"""
    
    # Guide Properties
    guide_size: bpy.props.FloatProperty = bpy.props.FloatProperty(
        name="Guide Size",
        description="Size of the guide objects",
        default=0.1,
        min=0.01,
        max=1.0
        )
    
    # Rig Properties
    bendy_joints: bpy.props.IntProperty = bpy.props.IntProperty(
        name="Bendy Joints",
        description="Number of bendy joints between main bones",
        default=0,
        min=0,
        max=3
    )
    
    stretch_controls: bpy.props.BoolProperty = bpy.props.BoolProperty(
        name="Stretch Controls",
        description="Add stretch controls to the rig",
        default=True
    )
    
    # Naming Convention
    naming_convention: bpy.props.EnumProperty =bpy.props.EnumProperty(
        name="Naming Convention",
        description="Choose the naming convention for bones",
        items=[
            ('DOTS', 'Dots (arm.L)', 'Use dots for separators: arm.L'),
            ('UNDERSCORE', 'Underscore (arm_L)', 'Use underscores: arm_L'),
            ('CAMELCASE', 'CamelCase (ArmL)', 'Use camel case: ArmL')
        ],
        default='DOTS'
    )
    
    # Chain Visibility
    show_spine: bpy.props.BoolProperty = bpy.props.BoolProperty(name="Spine Chain", default=True)
    show_arms: bpy.props.BoolProperty = bpy.props.BoolProperty(name="Arm Chains", default=True)
    show_legs: bpy.props.BoolProperty = bpy.props.BoolProperty(name="Leg Chains", default=True)
    show_fingers: bpy.props.BoolProperty = bpy.props.BoolProperty(name="Finger Chains", default=False)
    show_face: bpy.props.BoolProperty = bpy.props.BoolProperty(name="Face Rig", default=False)

class AUTORIGGER_OT_create_guides(ZenoBaseTool):
    """Create guide objects for rigging"""
    bl_idname = "auto_rigger.create_guides"
    bl_label = "Create Guides"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh_obj = context.active_object
        if not mesh_obj or mesh_obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object")
            return {'CANCELLED'}

        # Get mesh bounds for smart placement
        bounds = mesh_obj.bound_box
        center = mesh_obj.location
        height = max(v[2] for v in bounds) - min(v[2] for v in bounds)
        width = max(v[0] for v in bounds) - min(v[0] for v in bounds)

        # Create guides with relative positioning
        guides_data = [
            # Spine chain
            ("C_Root_Guide", Vector((0, 0, 0)) + center),
            ("C_Spine_01_Guide", Vector((0, 0, height * 0.2)) + center),
            ("C_Spine_02_Guide", Vector((0, 0, height * 0.4)) + center),
            ("C_Spine_03_Guide", Vector((0, 0, height * 0.6)) + center),
            
            # Left arm chain
            ("L_Shoulder_Guide", Vector((width * 0.2, 0, height * 0.8)) + center),
            ("L_Arm_Guide", Vector((width * 0.4, 0, height * 0.75)) + center),
            ("L_Forearm_Guide", Vector((width * 0.6, 0, height * 0.65)) + center),
            ("L_Hand_Guide", Vector((width * 0.8, 0, height * 0.6)) + center),
            
            # Right arm chain (mirrored)
            ("R_Shoulder_Guide", Vector((-width * 0.2, 0, height * 0.8)) + center),
            ("R_Arm_Guide", Vector((-width * 0.4, 0, height * 0.75)) + center),
            ("R_Forearm_Guide", Vector((-width * 0.6, 0, height * 0.65)) + center),
            ("R_Hand_Guide", Vector((-width * 0.8, 0, height * 0.6)) + center),
            
            # Left leg chain
            ("L_Hip_Guide", Vector((width * 0.1, 0, height * 0.35)) + center),
            ("L_Thigh_Guide", Vector((width * 0.15, 0, height * 0.25)) + center),
            ("L_Shin_Guide", Vector((width * 0.15, 0, height * 0.1)) + center),
            ("L_Foot_Guide", Vector((width * 0.15, 0.1, 0)) + center),
            
            # Right leg chain (mirrored)
            ("R_Hip_Guide", Vector((-width * 0.1, 0, height * 0.35)) + center),
            ("R_Thigh_Guide", Vector((-width * 0.15, 0, height * 0.25)) + center),
            ("R_Shin_Guide", Vector((-width * 0.15, 0, height * 0.1)) + center),
            ("R_Foot_Guide", Vector((-width * 0.15, 0.1, 0)) + center),
        ]

        for name, location in guides_data:
            guide = AutoRiggerTool.create_guide(name, location)
            # Add shrinkwrap constraint to snap to mesh
            constraint = guide.constraints.new(type='SHRINKWRAP')
            constraint.target = mesh_obj
            constraint.shrinkwrap_type = 'NEAREST_SURFACE'

        return {'FINISHED'}

class AUTORIGGER_OT_generate_rig(ZenoBaseTool):
    """Generate rig from guides"""
    bl_idname = "auto_rigger.generate_rig"
    bl_label = "Generate Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def get_guide_by_name(self, name):
        """Get guide object by name"""
        return bpy.data.objects.get(name)

    def create_bone_chain(self, armature, guide_names, bone_names):
        """Create a chain of bones from guides"""
        bones = []
        for i, (guide_name, bone_name) in enumerate(zip(guide_names, bone_names)):
            guide = self.get_guide_by_name(guide_name)
            if not guide:
                continue

            head = guide.location
            # If there's a next guide, use its location for tail
            if i < len(guide_names) - 1:
                next_guide = self.get_guide_by_name(guide_names[i + 1])
                tail = next_guide.location if next_guide else head + Vector((0, 0, 0.1))
            else:
                tail = head + Vector((0, 0, 0.1))

            parent_bone = bones[-1] if bones else None
            bone = AutoRiggerTool.create_bone(
                armature,
                bone_name,
                head,
                tail,
                parent_bone.name if parent_bone else None
            )
            bones.append(bone)
        return bones

    def execute(self, context):
        # Create main armature
        armature = AutoRiggerTool.create_armature("AutoRig")
        
        # Define bone chains
        chains = {
            "spine": {
                "guides": ["C_Root_Guide", "C_Spine_01_Guide", "C_Spine_02_Guide", "C_Spine_03_Guide"],
                "bones": ["C_Root_Bone", "C_Spine_01_Bone", "C_Spine_02_Bone", "C_Spine_03_Bone"]
            },
            "left_arm": {
                "guides": ["L_Shoulder_Guide", "L_Arm_Guide", "L_Forearm_Guide", "L_Hand_Guide"],
                "bones": ["L_Shoulder_Bone", "L_Arm_Bone", "L_Forearm_Bone", "L_Hand_Bone"]
            },
            "right_arm": {
                "guides": ["R_Shoulder_Guide", "R_Arm_Guide", "R_Forearm_Guide", "R_Hand_Guide"],
                "bones": ["R_Shoulder_Bone", "R_Arm_Bone", "R_Forearm_Bone", "R_Hand_Bone"]
            },
            "left_leg": {
                "guides": ["L_Hip_Guide", "L_Thigh_Guide", "L_Shin_Guide", "L_Foot_Guide"],
                "bones": ["L_Hip_Bone", "L_Thigh_Bone", "L_Shin_Bone", "L_Foot_Bone"]
            },
            "right_leg": {
                "guides": ["R_Hip_Guide", "R_Thigh_Guide", "R_Shin_Guide", "R_Foot_Guide"],
                "bones": ["R_Hip_Bone", "R_Thigh_Bone", "R_Shin_Bone", "R_Foot_Bone"]
            }
        }

        # Create all bone chains
        for chain in chains.values():
            self.create_bone_chain(armature, chain["guides"], chain["bones"])

        # Switch back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

class AUTORIGGER_OT_bind_mesh(ZenoBaseTool):
    """Bind mesh to generated rig"""
    bl_idname = "auto_rigger.bind_mesh"
    bl_label = "Bind Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh_obj = None
        armature_obj = None
        
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.select_get():
                mesh_obj = obj
            elif obj.type == 'ARMATURE' and obj.name == "AutoRig":
                armature_obj = obj

        if not (mesh_obj and armature_obj):
            self.report({'ERROR'}, "Please select the mesh and ensure the rig exists")
            return {'CANCELLED'}

        # Bind mesh to armature
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        armature_obj.select_set(True)
        context.view_layer.objects.active = armature_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')

        return {'FINISHED'}

class AUTORIGGER_PT_main_panel(bpy.types.Panel):
    """Main Auto Rigger Panel"""
    bl_label = "Auto Rigger"
    bl_idname = "AUTORIGGER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Auto Rigger'

    def draw(self, context):
        layout = self.layout
        props = context.scene.auto_rigger_props

        # Guide Creation Section
        box = layout.box()
        row = box.row()
        row.prop(props, "guide_size", text="Guide Size")
        box.operator("auto_rigger.create_guides", text="1. Create Guides")

        # Chain Visibility Section
        box = layout.box()
        box.label(text="Chain Visibility:")
        col = box.column(align=True)
        col.prop(props, "show_spine")
        col.prop(props, "show_arms")
        col.prop(props, "show_legs")
        col.prop(props, "show_fingers")
        col.prop(props, "show_face")

class AUTORIGGER_PT_settings_panel(bpy.types.Panel):
    """Settings Panel for Auto Rigger"""
    bl_label = "Rig Settings"
    bl_idname = "AUTORIGGER_PT_settings_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Auto Rigger'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.auto_rigger_props

        # Rig Generation Settings
        box = layout.box()
        box.label(text="Rig Generation Settings:")
        box.prop(props, "bendy_joints")
        box.prop(props, "stretch_controls")
        box.prop(props, "naming_convention")
        
        # Generate Rig Button
        box = layout.box()
        box.operator("auto_rigger.generate_rig", text="2. Generate Rig")

class AUTORIGGER_PT_binding_panel(bpy.types.Panel):
    """Binding Panel for Auto Rigger"""
    bl_label = "Mesh Binding"
    bl_idname = "AUTORIGGER_PT_binding_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Auto Rigger'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        
        # Mesh Binding Section
        box = layout.box()
        box.label(text="Mesh Binding:")
        box.operator("auto_rigger.bind_mesh", text="3. Bind Mesh")

        # Add button to remove binding
        box.operator("auto_rigger.clear_binding", text="Clear Binding")

class AUTORIGGER_OT_clear_binding(ZenoBaseTool):
    """Clear mesh binding"""
    bl_idname = "auto_rigger.clear_binding"
    bl_label = "Clear Binding"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.active_object and context.active_object.type == 'MESH':
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Please select the mesh object")
            return {'CANCELLED'}

# Update the classes list to include new UI classes
classes = [
    AutoRiggerProperties,
    AUTORIGGER_OT_create_guides,
    AUTORIGGER_OT_generate_rig,
    AUTORIGGER_OT_bind_mesh,
    AUTORIGGER_OT_clear_binding,
    AUTORIGGER_PT_main_panel,
    AUTORIGGER_PT_settings_panel,
    AUTORIGGER_PT_binding_panel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Register properties
    bpy.types.Scene.auto_rigger_props = bpy.props.PointerProperty(type=AutoRiggerProperties)

def unregister():
    # Unregister properties
    del bpy.types.Scene.auto_rigger_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
