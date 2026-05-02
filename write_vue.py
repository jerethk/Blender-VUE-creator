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
            a = obj.matrix_world[0][0]
            b = obj.matrix_world[1][0]
            c = obj.matrix_world[2][0]
            d = obj.matrix_world[0][1]
            e = obj.matrix_world[1][1]
            f = obj.matrix_world[2][1]
            g = obj.matrix_world[0][2]
            h = obj.matrix_world[1][2]
            i = obj.matrix_world[2][2]
            
            line = "transform \"{}\" {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:.2f} {:.2f} {:.2f}"
            file.write(line.format(obj.name, a, b, c, d, e, f, g, h, i, obj.location.x, obj.location.y, obj.location.z) + "\n")
            
        for obj in bpy.data.objects:
            if obj.type == 'CAMERA':
                x0 = obj.location.x
                z0 = obj.location.y
                y0 = obj.location.z
                
                # Blender's cameras point directly downward when unrotated, i.e. vector (0, 0, -1)
                vec_x = -10 * obj.matrix_world[0][2]
                vec_z = -10 * obj.matrix_world[1][2]
                vec_y = -10 * obj.matrix_world[2][2]
                x1 = x0 + vec_x
                z1 = z0 + vec_z
                y1 = y0 + vec_y
                
                # The format for camera lines is "camera x0 z0 y0 x1 z1 y1 roll ??"
                # The DF camera cannot be rolled so we will just set it to zero
                line = "camera {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} 0 0"
                file.write(line.format(x0, z0, y0, x1, z1, y1) + "\n")

                break   # only write 1 camera; if there are more, ignore them

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
