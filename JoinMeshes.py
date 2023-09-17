# Version: 2.0
import bpy
import os
from blender_3dmigoto_gimi import export_3dmigoto_genshin, Fatal
from bpy_extras.io_utils import ExportHelper
from bpy.utils import register_class, unregister_class
import subprocess
bl_info = {
    "name": "JoinMeshes",
    "blender": (2, 80, 0),
    "author": "LeoTorreZ / LeoMods",
    "location": "View3D > Sidebar > LeoTools",
    "description": "Facilitates the workflow when dealing with mods made in GIMI.",
    "category": "Interface",
    "tracker_url": "https://github.com/leotorrez/LeoTools",
}
class MainPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LeoTools"

    #bl_options = {"DEFAULT_CLOSED"}

class MyProperties(bpy.types.PropertyGroup):

    ExportFile: bpy.props.StringProperty(
        name="ExportFile",
        description="Export File:",
        default="",
        maxlen=1024,
        )
    use_foldername : bpy.props.BoolProperty(
        name="Use foldername when exporting",
        description="Sets the export name equal to the foldername you are exporting to. Keep true unless you have changed the names",
        default=True,
    )

    ignore_hidden : bpy.props.BoolProperty(
        name="Ignore hidden objects",
        description="Does not use objects in the Blender window that are hidden while exporting mods",
        default=False,
    )

    only_selected : bpy.props.BoolProperty(
        name="Only export selected",
        description="Uses only the selected objects when deciding which meshes to export",
        default=False,
    )

    no_ramps : bpy.props.BoolProperty(
        name="Ignore shadow ramps/metal maps/diffuse guide",
        description="Skips exporting shadow ramps, metal maps and diffuse guides",
        default=True,
    )

    delete_intermediate : bpy.props.BoolProperty(
        name="Delete intermediate files",
        description="Deletes the intermediate vb/ib files after a successful export to reduce clutter",
        default=True,
    )

    credit : bpy.props.StringProperty(
        name="Credit",
        description="Name that pops up on screen when mod is loaded. If left blank, will result in no pop up",
        default='',
    )

    outline_optimization : bpy.props.BoolProperty(
        name="Outline Optimization",
        description="Recalculate outlines. Recommended for final export. Check more options below to improve quality",
        default=False,
    )
    
    toggle_rounding_outline : bpy.props.BoolProperty(
        name="Round vertex positions",
        description="Rounding of vertex positions to specify which are the overlapping vertices",
        default=True,
    ) 
    
    decimal_rounding_outline : bpy.props.IntProperty(
        name="Decimals:",
        description="Rounding of vertex positions to specify which are the overlapping vertices",
        default=3,
    )

    angle_weighted : bpy.props.BoolProperty(
        name="Weight by angle",
        description="Calculate angles to improve accuracy of outlines",
        default=False,
    )

    overlapping_faces : bpy.props.BoolProperty(
        name="Ignore overlapping faces",
        description="Detect and ignore overlapping faces to avoid buggy outlines. Recommended if you have overlaps",
        default=False,
    )

    detect_edges : bpy.props.BoolProperty(
        name="Calculate edges",
        description="Calculate for disconnected edges when rounding, closing holes in the edge outline. Slow",
        default=False,
    )

    calculate_all_faces : bpy.props.BoolProperty(
        name="Calculate outline for all faces",
        description="If you have any flat shaded internal faces or if you just need to fix outline for all faces, turn on this option for better outlines. Slow",
        default=False,
    )

    nearest_edge_distance : bpy.props.FloatProperty(
        name="Distance:",
        description="Expand grouping for edge vertices within this radial distance to close holes in the edge outline. Requires rounding",
        default=0.001,
        soft_min=0,
        precision=4,
    )
    
class MY_PT_SelectStuffPanel(MainPanel,bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "MY_PT_SelectStuffPanel"
    bl_label = "Select Stuff Here you dummy :3"
    #    bl_label = "My Panel"
    #    bl_idname = "OBJECT_PT_my_panel"
    #    bl_space_type = 'PROPERTIES'
    #    bl_region_type = 'WINDOW'
    #    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        my_tool = context.scene.my_tool
        row = layout.row()

        split = layout.split(factor=0.75)
        col_1 = split.column()
        col_2 = split.column()
        col_1.prop(my_tool, "ExportFile")
        col_2.operator("export.selector", icon="FILE_FOLDER", text="")
        layout.separator()
       
        row = layout.row()
        row.operator("my.execute_auxclass", text="Export Mod")

        row = layout.row()

        row.operator("my.exportanimation", text="Export animation")

class WMFileSelector(bpy.types.Operator, ExportHelper):
    """Export single mod based on current frame"""
    bl_idname = "export.selector"
    bl_label = "Destination"
    
    filename_ext = "."
    use_filter_folder = True
    filter_glob : bpy.props.StringProperty(
            default='.',
            options={'HIDDEN'},
            )
    use_foldername : bpy.props.BoolProperty(
        name="Use foldername when exporting",
        description="Sets the export name equal to the foldername you are exporting to. Keep true unless you have changed the names",
        default=True,
    )

    ignore_hidden : bpy.props.BoolProperty(
        name="Ignore hidden objects",
        description="Does not use objects in the Blender window that are hidden while exporting mods",
        default=True,
    )

    only_selected : bpy.props.BoolProperty(
        name="Only export selected",
        description="Uses only the selected objects when deciding which meshes to export",
        default=False,
    )

    no_ramps : bpy.props.BoolProperty(
        name="Ignore shadow ramps/metal maps/diffuse guide",
        description="Skips exporting shadow ramps, metal maps and diffuse guides",
        default=True,
    )

    delete_intermediate : bpy.props.BoolProperty(
        name="Delete intermediate files",
        description="Deletes the intermediate vb/ib files after a successful export to reduce clutter",
        default=True,
    )

    credit : bpy.props.StringProperty(
        name="Credit",
        description="Name that pops up on screen when mod is loaded. If left blank, will result in no pop up",
        default='',
    )
    outline_optimization : bpy.props.BoolProperty(
        name="Outline Optimization",
        description="Recalculate outlines. Recommended for final export. Check more options below to improve quality",
        default=False,
    )
    
    toggle_rounding_outline : bpy.props.BoolProperty(
        name="Round vertex positions",
        description="Rounding of vertex positions to specify which are the overlapping vertices",
        default=True,
    ) 
    
    decimal_rounding_outline : bpy.props.IntProperty(
        name="Decimals:",
        description="Rounding of vertex positions to specify which are the overlapping vertices",
        default=3,
    )

    angle_weighted : bpy.props.BoolProperty(
        name="Weight by angle",
        description="Calculate angles to improve accuracy of outlines",
        default=False,
    )

    overlapping_faces : bpy.props.BoolProperty(
        name="Ignore overlapping faces",
        description="Detect and ignore overlapping faces to avoid buggy outlines. Recommended if you have overlaps",
        default=False,
    )

    detect_edges : bpy.props.BoolProperty(
        name="Calculate edges",
        description="Calculate for disconnected edges when rounding, closing holes in the edge outline. Slow",
        default=False,
    )

    calculate_all_faces : bpy.props.BoolProperty(
        name="Calculate outline for all faces",
        description="If you have any flat shaded internal faces or if you just need to fix outline for all faces, turn on this option for better outlines. Slow",
        default=False,
    )

    nearest_edge_distance : bpy.props.FloatProperty(
        name="Distance:",
        description="Expand grouping for edge vertices within this radial distance to close holes in the edge outline. Requires rounding",
        default=0.001,
        soft_min=0,
        precision=4,
    )
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        
        col.prop(self, 'use_foldername')
        col.prop(self, 'ignore_hidden')
        col.prop(self, 'only_selected')
        col.prop(self, 'no_ramps')
        col.prop(self, 'delete_intermediate')
        col.prop(self, 'credit')
        layout.separator()
        
        col = layout.column(align=True)
        col.prop(self, 'outline_optimization')
        
        if self.outline_optimization:
            col.prop(self, 'toggle_rounding_outline', text='Vertex Position Rounding', toggle=True, icon="SHADING_WIRE")
            col.prop(self, 'decimal_rounding_outline')
            col.prop(self, 'angle_weighted')
            col.prop(self, 'overlapping_faces')
            if self.toggle_rounding_outline:
                col.prop(self, 'detect_edges')
            if self.detect_edges and self.toggle_rounding_outline:
                col.prop(self, 'nearest_edge_distance')
            col.prop(self, 'calculate_all_faces')

    def execute(self, context):
        userpath = self.properties.filepath
        if not os.path.isdir(userpath):
            # attempt to remove file path 
            userpath = os.path.dirname(userpath)
            self.properties.filepath = userpath
            if not os.path.isdir(userpath):
                msg = "Please select a directory not a file\n" + userpath
                self.report({'WARNING'}, msg)

        context.scene.my_tool.ExportFile = self.properties.filepath    
        context.scene.my_tool.use_foldername = self.properties.use_foldername
        context.scene.my_tool.ignore_hidden = self.properties.ignore_hidden
        context.scene.my_tool.only_selected = self.properties.only_selected
        context.scene.my_tool.no_ramps = self.properties.no_ramps
        context.scene.my_tool.delete_intermediate = self.properties.delete_intermediate
        context.scene.my_tool.credit = self.properties.credit

        context.scene.my_tool.outline_optimization = self.properties.outline_optimization
        context.scene.my_tool.toggle_rounding_outline = self.properties.toggle_rounding_outline
        context.scene.my_tool.decimal_rounding_outline = self.properties.decimal_rounding_outline
        context.scene.my_tool.angle_weighted = self.properties.angle_weighted
        context.scene.my_tool.overlapping_faces = self.properties.overlapping_faces
        context.scene.my_tool.detect_edges = self.properties.detect_edges
        context.scene.my_tool.calculate_all_faces = self.properties.calculate_all_faces
        context.scene.my_tool.nearest_edge_distance = self.properties.nearest_edge_distance

        return{'FINISHED'}


class ExecuteAuxClassOperator(bpy.types.Operator):
    """Export full animation frame by frame. System console recomended."""
    bl_idname = "my.execute_auxclass_aux"
    bl_label = "Export Mod Aux"

    def exportframe(self,context,filename):
        scene = context.scene
        my_tool = scene.my_tool
        dirPath = os.path.dirname(my_tool.ExportFile)
        object_name = os.path.basename(dirPath)
        try:
            mainobjects = [obj for obj in scene.objects if obj.name.lower().startswith(object_name.lower()) and obj.visible_get() and obj.type == "MESH"]
            collectionstojoin = []
            for col in bpy.data.collections:
                for obj in mainobjects:
                    if obj.name.lower().startswith(col.name.lower()):
                        collectionstojoin.append(col)

            #skipping error check ign for now. trusting in gimi to solve it for me
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.make_single_user(type='ALL', object=True, obdata=True, animation=True, obdata_animation=True)
            for obj in mainobjects:
                print("Searching partner for "+obj.name)
                for col in collectionstojoin:
                    if obj.name.lower().startswith(col.name.lower()):
                        self.report({"WARNING"},"Found MATCH!")
                        col = bpy.data.collections[col.name]
                        self.joinInto(col, obj)
                        mainobjects.remove(obj)
                        collectionstojoin.remove(col)
                        break
                self.report({'WARNING'},"Collection not found for object: " + obj.name)
            if len(mainobjects) > 0:
                print("Warning: some objects were ignored. or had no match.")
                print("Objects ignored: ")
                for obj in mainobjects:
                    print(obj.name)
            if len(collectionstojoin) > 0:
                print("Warning: some collections were ignored. or had no match.")
                print("Collections ignored: ")
                for col in collectionstojoin:
                    print(col.name)

            filepath = dirPath + "/" + object_name + ".vb"
            if(filename is not None):
                path=dirPath
                filepath = path +"/"+ filename
            vb_path = filepath
            ib_path = os.path.splitext(vb_path)[0] + '.ib'
            fmt_path = os.path.splitext(vb_path)[0] + '.fmt'

            Outline_Properties = (my_tool.outline_optimization, my_tool.toggle_rounding_outline, my_tool.decimal_rounding_outline, my_tool.angle_weighted, my_tool.overlapping_faces, my_tool.detect_edges, my_tool.calculate_all_faces, my_tool.nearest_edge_distance)
            export_3dmigoto_genshin(self, context, object_name, vb_path, ib_path, fmt_path, my_tool.use_foldername, my_tool.ignore_hidden, my_tool.only_selected, my_tool.no_ramps, my_tool.delete_intermediate, my_tool.credit,Outline_Properties)
            bpy.ops.ed.undo_push(message="Joining Meshes and Exporting Mod Folder")
            bpy.ops.ed.undo()
        except Fatal as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}
    def execute(self, context):
        #bpy.ops.ed.undo_push(message="Exporting mod!")
        self.exportframe(bpy.context, None)

        
        return {'FINISHED'}
        
    def appendto(self, collection, destination):
        for a_collection in collection.children:
            self.appendto(a_collection, destination)
        for obj in collection.objects:
            if obj.type == "MESH":
                destination.append(obj)

    def joinInto(self, collection_name, object):
        target_obj_name=object.name
        target_obj = bpy.data.objects[target_obj_name]
        objects_to_join = []
        if collection_name is not None:
            collection_obj = bpy.data.collections[collection_name.name]
            #recursively appends elements within the collection
            self.appendto(collection_obj, objects_to_join)

        #select main object then selecting all the meshes to join into it
        bpy.data.objects[target_obj_name].select_set(True)
        if len(objects_to_join) > 0:
            for obj in objects_to_join:
                obj.select_set(True)
        #apply shapekeys
        context = bpy.context
        objs = context.selected_objects
        for ob in objs:
            ob.hide_viewport = False  # should be visible
            if ob.data.shape_keys:
                 ob.shape_key_add(name='CombinedKeys', from_mix=True)
                 for shapeKey in ob.data.shape_keys.key_blocks:
                     ob.shape_key_remove(shapeKey)
        #apply modifierss
        for obj in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = obj
            for modifier in obj.modifiers:
                if not modifier.show_viewport:
                    obj.modifiers.remove(modifier)
                else:
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
                
        bpy.context.view_layer.objects.active = target_obj
        #join
        bpy.ops.object.join()
        target_obj.data = bpy.context.object.data
        
        #quick fix to remove all vertex groups with the word MASK on them
        #lacks user interface and feedback 
        ob = target_obj
        vgs = [vg for vg in ob.vertex_groups
               if vg.name.find("MASK") != -1]
        while(vgs):
            ob.vertex_groups.remove(vgs.pop())
            
        #deselect everything and set result as active
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = target_obj
        return {'FINISHED'}

class MY_OT_ExecuteAuxClassOperator(ExecuteAuxClassOperator):
    bl_idname = "my.execute_auxclass"
    bl_label = "Export Mod"
class ExportAnimationOperator(ExecuteAuxClassOperator):
    """Operator to execute the auxClass"""
    bl_idname = "my.exportanimation"
    bl_label = "Export animation"

    def execute(self,context):
        bpy.ops.ed.undo_push(message="Exporting Animation!")
        scene = context.scene
        my_tool = scene.my_tool        
        dirPath = os.path.dirname(my_tool.ExportFile)
        object_name = os.path.basename(dirPath)
        filepath = dirPath+"/"+object_name+".vb"

        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end
        print("starting animation exporting Loop")
        for f in range(frame_start, frame_end + 1):
            bpy.context.scene.frame_set(f)
            filename = "%sf%04d.vb" % (object_name, f)
            self.exportframe(bpy.context, filename)
            
            dirname = os.path.dirname(filepath)+"Mod"
            new = dirname+"f%04d" % f
            
            if os.path.exists(new):
                os.remove(new)
            os.rename(dirname, new)
            print("exported: "+filename)
        
        directory = os.path.dirname(os.path.dirname(filepath))
        newfile_name = os.path.join( directory , "genshin_merge_mods.py")
        newfile_name2 = os.path.join( directory , "speedControl.py")

        file1_args = ["-c","-k y"]
        file2_args = ["-s {}".format(frame_start), "-e {}".format(frame_end)]
        file1_command = ["python", newfile_name] + file1_args
        file2_command = ["python", newfile_name2] + file2_args
        try:
            file1_process = subprocess.Popen(file1_command, stdin=subprocess.PIPE, cwd=directory)
            file1_process.communicate(input=b"\n")
            file1_process.wait()
            subprocess.run(file2_command, check=True, stdin=subprocess.PIPE, cwd=directory)
        except subprocess.CalledProcessError as e:
            print(f"Error running file2.py: {e}")
        return {'FINISHED'}
    
classes = (
    MyProperties,
    MY_PT_SelectStuffPanel,
    ExecuteAuxClassOperator,
    MY_OT_ExecuteAuxClassOperator,
    WMFileSelector,
    ExportAnimationOperator
)
def register():
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)    

def unregister():
    del bpy.types.Scene.my_tool
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()