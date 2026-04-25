import bpy
import math


def write_vue(context, filepath):
    scene = bpy.context.scene

    file = open(filepath, 'w', encoding='utf-8')
    file.write("VUE \n")

    for f in range(scene.frame_end):
        scene.frame_set(f)
        file.write("\n")
        file.write("frame {} \n".format(f))

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue # skip non-mesh objects
            
            pch = -obj.rotation_euler.x 
            yaw = -obj.rotation_euler.z
            rol = -obj.rotation_euler.y
            a = math.cos(yaw) * math.cos(rol) - math.sin(yaw) * math.sin(pch) * math.sin(rol)
            b = -math.cos(pch) * math.sin(yaw)
            c = math.cos(yaw) * math.sin(rol) + math.cos(rol) * math.sin(yaw) * math.sin(pch)
            d = math.cos(rol) * math.sin(yaw) + math.cos(yaw) * math.sin(pch) * math.sin(rol)
            e = math.cos(yaw) * math.cos(pch)
            f = math.sin(yaw) * math.sin(rol) - math.cos(yaw) * math.cos(rol) * math.sin(pch)
            g = -math.cos(pch) * math.sin(rol)
            h = math.sin(pch)
            i = math.cos(pch) * math.cos(rol)
            
            line = "transform \"{}\" {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:.2f} {:.2f} {:.2f}"
            file.write(line.format(obj.name, a, b, c, d, e, f, g, h, i, obj.location.x, obj.location.y, obj.location.z) + "\n")
            
    file.close()
    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportVue(Operator, ExportHelper):
    """Create a VUE file."""
    bl_idname = "export_.vue"
    bl_label = "Create VUE"

    # ExportHelper mixin class uses this
    filename_ext = ".vue"

    filter_glob: StringProperty(
        default="*.vue",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_vue(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="Text Export Operator")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(ExportVue)
    #bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportVue)
    #bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
