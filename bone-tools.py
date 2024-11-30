import bpy
from bpy.types import (Panel, Operator)
import functools
import time

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class CopyWeights(Operator):
    """Copy weights from selected bones to active bone"""
    bl_idname = "object.copy_weights"
    bl_label = "Copy weights from selected bones to active bone, and delete bones"
    
    def copy_weights(self, context, sources, target):
        for bone in sources:
            bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')    
            bpy.context.object.modifiers["VertexWeightMix"].vertex_group_a = target.name
            bpy.context.object.modifiers["VertexWeightMix"].vertex_group_b = bone.name
            bpy.context.object.modifiers["VertexWeightMix"].mix_set = 'ALL'
            bpy.context.object.modifiers["VertexWeightMix"].mix_mode = 'MAX'
            try:
                bpy.ops.object.modifier_apply(modifier="VertexWeightMix", report=True)
            except:
                bpy.ops.object.modifier_remove(modifier="VertexWeightMix", report=True)

    
    def done(self, current_active, current_mode):
        bpy.context.view_layer.objects.active = current_active
        bpy.ops.object.mode_set ( mode = current_mode ) 

        return {'FINISHED'}

    def execute(self, context):
        all_source_bones = []
        source_bones = []
        target_bone = context.active_pose_bone
    
        for bone in bpy.context.selected_pose_bones:
            if bone.name == target_bone.name:
                continue
            source_bones.append(bone)
            all_source_bones.append(bone)
        
        while True:
            if len(source_bones) == 0:
                break

            self.copy_weights(context, source_bones, target_bone)

            if(len(target_bone.children) != 0):
                target_bone = target_bone.children[0]

            oldSourceBones = source_bones
            source_bones = []

            for bone in oldSourceBones:
                for child in bone.children:
                    source_bones.append(child)
                    all_source_bones.append(child)


        current_mode = bpy.context.object.mode
        current_active = bpy.context.view_layer.objects.active
       # print(target_bone.name)

        
        armature = bpy.context.active_pose_bone.id_data
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        
        edit_bones = armature.data.edit_bones
        for bone in all_source_bones:
            if bone.name in edit_bones:
                edit_bones.remove(edit_bones[bone.name])
                print('Deleted bone:', bone.name)

        bpy.ops.object.mode_set(mode='OBJECT')
       # bpy.app.timers.register(functools.partial(self.done, current_active, current_mode), first_interval=1)     


        bpy.context.view_layer.objects.active = current_active
        bpy.ops.object.mode_set ( mode = current_mode ) 

        context.area.tag_redraw()
        context.region.tag_redraw()
        #armature.modifiers.update()
        #armature.update_tag()
        #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}
# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------


class FixGroups(Operator):
    """Fix Groups"""
    bl_idname = "object.fix_groups"
    bl_label = "Copy weights from underscore [_] notation groups to dot notation groups [.] (bone_1 to bone.1 (if bone.1 exists))"
    
    def copy_weights(self, source, target):
        bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')    
        bpy.context.object.modifiers["VertexWeightMix"].vertex_group_a = target
        bpy.context.object.modifiers["VertexWeightMix"].vertex_group_b = source
        bpy.context.object.modifiers["VertexWeightMix"].mix_set = 'ALL'
        bpy.context.object.modifiers["VertexWeightMix"].mix_mode = 'MAX'
        try:
            bpy.ops.object.modifier_apply(modifier="VertexWeightMix", report=True)
        except:
            bpy.ops.object.modifier_remove(modifier="VertexWeightMix", report=True)

    
    def done(self, current_active, current_mode):
        bpy.context.view_layer.objects.active = current_active
        bpy.ops.object.mode_set ( mode = current_mode ) 

        return {'FINISHED'}

    def execute(self, context):
        source_bones = []
    
        for bone1 in bpy.context.selected_pose_bones:
            if bone1.name != bone1.name.replace('.', '_'):
                print('trying:', bone1.name.replace('.', '_'), bone1.name)
                self.copy_weights(bone1.name.replace('.', '_'), bone1.name)
                continue
       
        context.area.tag_redraw()
        context.region.tag_redraw()
        return {'FINISHED'}


class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "object.custom_panel"
    bl_label = "My Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "weightpaint"

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        obj = context.object

        layout.label(text="Properties:")
    
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(obj, "show_name", toggle=True, icon="FILE_FONT")
        row.prop(obj, "show_wire", toggle=True, text="Wireframe", icon="SHADING_WIRE")
        col.prop(obj, "show_all_edges", toggle=True, text="Show all Edges", icon="MOD_EDGESPLIT")
        layout.separator()

        layout.label(text="Operators:")

        col = layout.column(align=True)
        col.operator(CopyWeights.bl_idname, text="Copy weights", icon="CONSOLE")
        col.operator(FixGroups.bl_idname, text="Gix weight groups", icon="CONSOLE")

        layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(OBJECT_PT_CustomPanel)
    bpy.utils.register_class(CopyWeights)
    bpy.utils.register_class(FixGroups)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    bpy.utils.unregister_class(CopyWeights)
    bpy.utils.unregister_class(FixGroups)

if __name__ == "__main__":
    register()