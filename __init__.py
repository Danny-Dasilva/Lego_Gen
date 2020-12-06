'''
Copyright (C) 2020 Nicolas Jarraud
mecabricks@gmail.com
Created by Nicolas jarraud
    License of the software is non-exclusive, non-transferrable
    and is granted only to the original buyer. Buyers do not own
    any Product and are only licensed to use it in accordance
    with terms and conditions of the applicable license. The Seller
    retains copyright in the software purchased or downloaded by any Buyer.
    The Buyer may not resell, redistribute, or repackage the Product
    without explicit permission from the Seller.
    Any Product, returned to Mecabricks and (or) the Seller in accordance
    with applicable law for whatever reason must be destroyed by the Buyer
    immediately. The license to use any Product is revoked at the time
    Product is returned. Product obtained by means of theft or fraudulent
    activity of any kind is not granted a license.
'''

bl_info = {
    "name": "Mecabricks Lite",
    "description": "Import Mecabricks 3D Models",
    "author": "Nicolas Jarraud",
    "version": (3, 1, 3),
    "blender": (2, 81, 0),
    "location": "File > Import-Export",
    "warning": "",
    "wiki_url": "www.mecabricks.com",
    "category": "Import-Export"
}

import bpy
import os
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from .loaders.SceneLoader import SceneLoader
from .loaders.utils import find_node
############################
from random import uniform, randint
# ------------------------------------------------------------------------------
# Import Mecabricks scene
# ------------------------------------------------------------------------------
def import_mecabricks(self, context, filepath, settings):
    # Check Blender version
    if bpy.app.version < (2, 81, 0):
        self.report({'ERROR'}, 'This add-on requires Blender 2.81 or greater.')
        return {'FINISHED'}

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Create new collection
    collection_name = os.path.splitext(os.path.basename(filepath))[0]
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # Addon directory path
    addon_path = os.path.dirname(os.path.realpath(__file__))

    # Load scene
    loader = SceneLoader(addon_path, settings['logos'])
    scene = loader.load(filepath, collection)

    # Focus viewports
    focus_viewports(scene['parts'])

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select empty
    scene['empty'].select_set(state=True)
    bpy.context.view_layer.objects.active = scene['empty']

    return {'FINISHED'};


def import_mecabricks_for_panel(self, context, filepath, settings):
    # Check Blender version
    if bpy.app.version < (2, 81, 0):
        self.report({'ERROR'}, 'This add-on requires Blender 2.81 or greater.')
        return {'FINISHED'}

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Create new collection
    collection_name = os.path.splitext(os.path.basename(filepath))[0]
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # Addon directory path
    addon_path = os.path.dirname(os.path.realpath(__file__))

    # Load scene
    loader = SceneLoader(addon_path, settings['logos'])
    scene = loader.load(filepath, collection)

    # Focus viewports
    focus_viewports(scene['parts'])

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select empty
    scene['empty'].select_set(state=True)
    bpy.context.view_layer.objects.active = scene['empty']

    
    objects = bpy.data.objects
    object_list = []
    for obj in objects:
        if 'part' in obj.name:
            object_list.append(obj)
    print(object_list)
    return object_list

# ------------------------------------------------------------------------------
# Focus viewport cameras on added elements
# ------------------------------------------------------------------------------
def focus_viewports(objects):
    # Select added objects
    for object in objects:
        object.select_set(state=True)

    # Focus viewport on scene for all 3D views
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D' and area.spaces[0].region_3d.view_perspective != 'CAMERA':
            ctx = bpy.context.copy()
            ctx['area'] = area
            ctx['region'] = area.regions[-1]
            bpy.ops.view3d.view_selected(ctx)

# ------------------------------------------------------------------------------
# Import panel
# ------------------------------------------------------------------------------
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator

class IMPORT_OT_zmbx(Operator, ImportHelper):
    bl_idname = 'import_mecabricks.zmbx'
    bl_description = 'Import from Mecabricks file format (.zmbx)'
    bl_label = "Import ZMBX"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_options = {'UNDO'}

    filepath: StringProperty(
        name="input file",
        subtype='FILE_PATH'
    )

    filename_ext = ".zmbx"

    filter_glob: StringProperty(
        default = "*.zmbx",
        options = {'HIDDEN'},
    )

    # Logos
    setting_logos: BoolProperty(
            name="Logo on studs",
            description="Display brand logo on top of studs",
            default=True,
            )

    def draw(self, context):
        layout = self.layout

        # Geometry
        box = layout.box()
        box.label(text='Geometry Options: ', icon="OUTLINER_DATA_MESH" )

        # Logos
        row = box.row()
        row.prop(self.properties, 'setting_logos')

    def execute(self, context):
        settings = {
            'logos': self.setting_logos
        }
        print(self.filepath)
        return import_mecabricks(self, context, self.filepath, settings)


def delete_legos():
    collections = [ c.name for c in bpy.data.collections if c.name != "Collection 1" ]
    for name in collections:
        remove_collection_objects = True

        coll = bpy.data.collections.get(name)

        if coll:
            if remove_collection_objects:
                obs = [o for o in coll.objects if o.users == 1]
                while obs:
                    bpy.data.objects.remove(obs.pop())

            bpy.data.collections.remove(coll)
    
    #clear data
    for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)


def randomize_position(objs: list, x: int, y: int, z: int):
    pi = 3.14
    for obj in objs:

        roll = uniform(0, 360)
        pitch = uniform(0, 360)
        yaw = uniform(0, 360)
        obj.rotation_mode = 'XYZ'
        obj.rotation_euler[0] = pitch*(pi/180.0)
        obj.rotation_euler[1] = roll*(pi/180)
        obj.rotation_euler[2] = yaw*(pi/180.0)
        
        obj.location.x = uniform(-x, x)
        obj.location.y = uniform(-y, y)
        obj.location.z = z

def assign_physics(objs, passive: str):
    for obj in objs:
        
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.mass = 1000000

        bpy.context.object.rigid_body.collision_shape = 'MESH'
        obj.select_set(True) 
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        
    bpy.ops.object.select_all(action='DESELECT')
    object = bpy.data.objects[passive]
    bpy.context.view_layer.objects.active = object
    object.select_set(True) 
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = 'PASSIVE'
    bpy.context.object.rigid_body.collision_shape = 'BOX'
    bpy.ops.object.select_all(action='DESELECT')



def increment_frames(scene, frames):
    for i in range(frames):
        scene.frame_set(i)

def render(scene, name, image_count):
    file_format = scene.render.image_settings.file_format.lower()
    image_dir = "./images/"
    for count in range(image_count):


        
        print(count)
        filename = f'{name}-{str(count)}.{file_format}'

        #write image out
        bpy.context.scene.render.filepath = f'{image_dir}{filename}'
        bpy.ops.render.render(write_still=True)

def update():
        dg = bpy.context.evaluated_depsgraph_get() 
        dg.update()
class OT_Execute(Operator):
    bl_idname = "scene.execute_operator"
    bl_label = "Spawn Legos"

    
    def execute(self, context):
        scene = context.scene
        mytool = context.scene.my_tool
        settings = mytool.setting_logos

        settings = {
            'logos': mytool.setting_logos
        }


        import glob, os
        filepath = bpy.path.abspath(mytool.filepath)
        os.chdir(filepath)
        for fl in glob.glob("*.zmbx"):
            path = f"{filepath}{fl}"
            objs = import_mecabricks_for_panel(self, context, path, settings)
    
            assign_physics(objs, 'Base')
            
            image_count = 10
            file_format = scene.render.image_settings.file_format.lower()
            image_dir = "./images/"
            for count in range(image_count):
                scene.frame_set(0)
                randomize_position(objs, 45, 35, 70)

                
                print(count)
                name = fl.split('.')[0]
                increment_frames(scene, 300)
                filename = f'{name}-{str(count)}.{file_format}'

                #write image out
                bpy.context.scene.render.filepath = f'{image_dir}{filename}'
                bpy.ops.render.render(write_still=True)
        

            #cleanup                
            delete_legos()
        
        

        return {'FINISHED'}

class OT_Delete(Operator):
    bl_idname = "scene.delete_operator"
    bl_label = "Delete legos"

    def execute(self, context):
        delete_legos()
        return {'FINISHED'}    


class MyProperties(PropertyGroup):

    filepath: StringProperty(
        name="input file",
        subtype='FILE_PATH'
    )
    # Logos
    setting_logos: BoolProperty(
            name="Logo on studs",
            description="Display brand logo on top of studs",
            default=True,
            )




class Create_Data(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category = "Gen Lego"
       
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = scene.my_tool

        # Logos
        row = layout.row()
        row.prop(tool, 'setting_logos')

        layout.prop(tool, "filepath")

        layout.operator("scene.execute_operator")

        layout.operator("scene.delete_operator")



# ------------------------------------------------------------------------------
# Register / Unregister
# ------------------------------------------------------------------------------
# Import menu
def menu_func(self, context):
    self.layout.operator(IMPORT_OT_zmbx.bl_idname, text = 'Mecabricks (.zmbx)')
classes = (
    IMPORT_OT_zmbx,
    Create_Data,
    MyProperties,
    OT_Execute,
    OT_Delete
)
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)
        
    bpy.types.TOPBAR_MT_file_import.append(menu_func)
    
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls) 
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)
    del bpy.types.Scene.my_tool
if __name__ == "__main__":
    register()
