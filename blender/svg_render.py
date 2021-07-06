import bpy
import json

from mathutils import Vector
def setup_grease(first_part):
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), type='STROKE')
    bpy.context.area.type = 'VIEW_3D'
    bpy.data.objects['Stroke'].select_set(True)
    bpy.ops.gpencil.editmode_toggle()
    bpy.ops.gpencil.select_all(action='SELECT')
    bpy.ops.gpencil.delete(type='POINTS')
    bpy.ops.gpencil.editmode_toggle()
    bpy.context.area.type = 'TEXT_EDITOR'

    #add material to object
    bpy.ops.object.gpencil_modifier_add(type='GP_LINEART')
    bpy.context.object.grease_pencil_modifiers["Line Art"].source_type = 'OBJECT'
    bpy.context.object.grease_pencil_modifiers["Line Art"].use_remove_doubles = True
    bpy.context.object.grease_pencil_modifiers["Line Art"].source_object = first_part
    bpy.context.object.grease_pencil_modifiers["Line Art"].target_layer = "Lines"
    black_material_name = bpy.data.objects['Stroke'].material_slots[0].name
    bpy.context.object.grease_pencil_modifiers["Line Art"].target_material = bpy.data.materials[black_material_name]
    bpy.context.object.show_in_front = True

#bpy.data.objects['Stroke'].select_set(True)
#bpy.context.object.grease_pencil_modifiers["Line Art"].source_object = bpy.data.objects["Cube"]


#bpy.ops.wm.gpencil_export_svg(filepath='/your/filepath/test.svg')

def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()

with open('./Mecabricks/my-downloads/filenames.json') as f:
  part_names = json.load(f)

def rename_parts(filename):
    for col in bpy.data.collections:
        if col.name == filename:
            rename_list = [obj for obj in col.objects if obj.type == 'MESH']
            for count, obj in enumerate(rename_list):
                obj.name = part_names[count]
            obj_list = [obj for obj in col.objects if obj.type == 'MESH']
            return obj_list


def scale(filename):
    
    bpy.ops.object.select_all(action='DESELECT')
    for col in bpy.data.collections:
        if col.name == filename:
            for obj in col.objects:
                obj.select_set(True)
                bpy.ops.transform.resize(value=(.3, .3, .3))
#                 bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
                obj.select_set(False)
                
                
    bpy.ops.object.select_all(action='DESELECT')

def get_objects(filename):
    for col in bpy.data.collections:
            if col.name == filename:
                
                obj_list = [obj for obj in col.objects if obj.type == 'MESH']
                return obj_list
from time import sleep            
def render(camera, parts):
    print("render")
    for render_count, part in enumerate(parts):
        bpy.ops.object.select_all(action='DESELECT')
        part.hide_set(False)
        modifier = 2
        x = abs(part.dimensions.x)
        y = abs(part.dimensions.y)
        z = abs(part.dimensions.z)
        distance = max(x, y, z)
        camera.location.x = distance*modifier
        camera.location.y = -distance*modifier
        camera.location.z = distance*modifier
        print(z, camera.rotation_euler)
        camera.select_set(True)
        look_at(camera, Vector((0,0,z/2)))
        camera.select_set(False)
        print(z, camera.rotation_euler)
        bpy.data.objects['Stroke'].select_set(True)
        bpy.context.object.grease_pencil_modifiers["Line Art"].source_object = part
        path = f"./test/{part.name}.svg"
        bpy.ops.wm.gpencil_export_svg(filepath=path)
        bpy.data.objects['Stroke'].select_set(False)
        
        part.hide_set(True)
        
def hide_parts(parts, hide=True):
    for part in parts:
        part.hide_set(hide)

def cleanup():
    hide_parts(parts, hide=False)
    bpy.data.objects['Stroke'].select_set(True)
    bpy.ops.object.delete() 

def search(values, searchFor):
    for k in values:
        for v in values[k]:
            if searchFor in v:
                return k
    return None

#rename_parts('all_parts')
#scale('all_parts')

#sleep(.1)
camera = bpy.data.objects['Camera']

parts = get_objects('all_parts')
setup_grease(parts[0])
hide_parts(parts)
render(camera, parts)
#cleanup()
#print("hello")
#for render_count, part in enumerate(parts):
#    print(part)