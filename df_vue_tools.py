import bpy
from bpy.types import Panel, Operator, PropertyGroup, Object
from bpy.props import IntProperty, PointerProperty, FloatProperty
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
     
        
        grid.operator("addonname.myop_operator1")
        grid.operator("addonname.myop_operator2")
        grid.operator("addonname.myop_operator3")
        grid.operator("addonname.myop_operator4")
        grid.operator("addonname.myop_operator5")




class ADDONNAME_OT_my_op1(Operator):
    """Import a Dark Forces 3DO object file into Blender"""
    bl_label = "Import .3DO"
    bl_idname = "addonname.myop_operator1"
        
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        s = random.choice(range(0, 40))
        bpy.data.objects["Cube"].scale[0] = s*0.1
    
        return {'FINISHED'}
    
    
    
class ADDONNAME_OT_my_op2(Operator):
    """Import a Dark Forces .LEV level file into Blender"""
    bl_label = "Import .LEV"
    bl_idname = "addonname.myop_operator2"
        
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        


    
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



classes = [MyProperties,ADDONNAME_PT_main_panel, ADDONNAME_OT_my_op1, ADDONNAME_OT_my_op2, ADDONNAME_OT_my_op3, ADDONNAME_OT_my_op4, ADDONNAME_OT_my_op5]
 
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.my_tool = PointerProperty(type= MyProperties)


 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.my_tool


 
 
if __name__ == "__main__":
    register()