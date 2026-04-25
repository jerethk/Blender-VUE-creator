import bpy
from bpy.types import Panel, Operator, PropertyGroup, Object
from bpy.props import IntProperty, PointerProperty, FloatProperty, BoolProperty
import bpy.utils.previews
from bpy.utils import register_class, unregister_class, previews
import random


class MyProperties(PropertyGroup):
    
        random_number : bpy.props.IntProperty(name= "Random Number", default=1, min =1, max =200)


class ADDONNAME_PT_main_panel(Panel):
    bl_label = "Dark Forces VUE Tools"
    bl_idname = "ADDONNAME_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DF Tools"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
                        
        col = self.layout.box().column()
                        
        grid = col.grid_flow(columns=1, align=True)
        
        grid.operator("addonname.myop_import3do")
        grid.operator("addonname.myop_importlev")
        grid.operator("addonname.myop_operator3")
        grid.operator("addonname.myop_operator5")

        layout.row().label(text="Currently selected objects:")

        # Show a checkbox for each object representing whether it is selected
        for obj in bpy.data.objects:
            if obj.type != 'MESH':
                continue
            row = layout.row()
            row.prop(obj, "is_selected")
            row.label(text=obj.name)
        


class ADDONNAME_OT_Import3do(Operator):
    """Import a Dark Forces 3DO object file into Blender"""
    bl_label = "Import .3DO"
    bl_idname = "addonname.myop_import3do"
        
    def execute(self, context):
        scene = context.scene
        bpy.ops.import_vue.df3do('INVOKE_DEFAULT')
    
        return {'FINISHED'}
    
    
    
class ADDONNAME_OT_ImportLev(Operator):
    """Import a Dark Forces .LEV level file into Blender"""
    bl_label = "Import .LEV"
    bl_idname = "addonname.myop_importlev"
        
    def execute(self, context):
        scene = context.scene
        bpy.ops.import_vue.dflev('INVOKE_DEFAULT')

    
        return {'FINISHED'}
    
    
    
class ADDONNAME_OT_my_op3(Operator):
    """Bake all animations and constraints on the selected object to keyframes"""
    bl_label = "Bake Keyframes on Selected"
    bl_idname = "addonname.myop_operator3"
        
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        

        bpy.ops.nla.bake(frame_start=1, frame_end=250, visual_keying=True, clear_constraints=True, clear_parents=True, use_current_action=True, bake_types={'OBJECT'})

    
        return {'FINISHED'}
    
    
    
class ADDONNAME_OT_my_op4(Operator):
    """Export the active object only as a .VUE animation data file for Dark Forces"""
    bl_label = "Export Active (Single) .VUE"
    bl_idname = "addonname.myop_operator4"
        
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        


    
        return {'FINISHED'}
    
    
    
class ADDONNAME_OT_my_op5(Operator):
    """Export the selected objects as a .VUE animation data file for Dark Forces"""
    bl_label = "Export Selected (Multiple) .VUE"
    bl_idname = "addonname.myop_operator5"
        
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        


    
        return {'FINISHED'}



classes = [MyProperties, ADDONNAME_PT_main_panel, ADDONNAME_OT_Import3do, ADDONNAME_OT_ImportLev, ADDONNAME_OT_my_op3, ADDONNAME_OT_my_op4, ADDONNAME_OT_my_op5]
 
 
def register():
    bpy.data.texts["import_lev.py"].as_module().register()
    bpy.data.texts["import3do.py"].as_module().register()

    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.my_tool = PointerProperty(type= MyProperties)
    
    # Add a custom is_selected property to objects
    bpy.types.Object.is_selected = BoolProperty(name="", get=lambda self: self.select_get() == True, set=lambda self, value: self.select_set(value))


 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.my_tool
    del bpy.types.Object.is_selected


 
 
if __name__ == "__main__":
    register()
