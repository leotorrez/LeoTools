'''Join Meshes is a script to enhance XXMI mod making workflows.'''
import os
import shutil
import subprocess
import re
from threading import Timer

import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, StringProperty
from bpy.types import Context, UIList, PropertyGroup, Operator
from bpy_extras.io_utils import ExportHelper
IS_SRMI = True
try:
    from blender_3dmigoto_srmi import export_3dmigoto_genshin
except ModuleNotFoundError as err:
    from blender_3dmigoto_gimi import export_3dmigoto_genshin
    IS_SRMI = False

bl_info = {
    "name": "JoinMeshes",
    "blender": (2, 80, 0),
    "author": "LeoTorreZ / LeoMods",
    "location": "View3D > Sidebar > LeoTools",
    "description": "Facilitates the workflow when dealing with mods made in XXMI.",
    "category": "Interface",
    "tracker_url": "https://github.com/leotorrez/LeoTools",
    "version": (3, 0, 0),
}
class MainPanel:
    '''Main Panel'''
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LeoTools"
class CUSTOM_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    obj_type: StringProperty()
    obj_id: IntProperty()
    arguments: StringProperty()
class MyProperties(bpy.types.PropertyGroup):
    '''Properties for the addon'''
    ExportFile: bpy.props.StringProperty(name="Dump Folder", description="Dump Folder:",
                                         default="", maxlen=1024,)
    OutputFile: bpy.props.StringProperty(name="Output Folder", description="Output Folder:",
                                         default="", maxlen=1024,)
    use_foldername : bpy.props.BoolProperty(name="Use foldername when exporting", default=True,
        description='''Sets the export name equal to the foldername you are exporting to.
        Keep true unless you have changed the names''',)
    ignore_hidden : bpy.props.BoolProperty(name="Ignore hidden objects", default=False,
        description="Does not use objects in the Blender window that are hidden while exporting mods",)
    only_selected : bpy.props.BoolProperty(name="Only export selected", default=False,
        description="Uses only the selected objects when deciding which meshes to export", )
    no_ramps : bpy.props.BoolProperty(name="Ignore shadow ramps/metal maps/diffuse guide", default=True,
        description="Skips exporting shadow ramps, metal maps and diffuse guides",)
    delete_intermediate : bpy.props.BoolProperty(name="Delete intermediate files", default=True,
        description="Deletes the intermediate vb/ib files after a successful export to reduce clutter", )
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
    star_rail : bpy.props.BoolProperty(name="Star Rail",default=False,
        description="Export as Star Rail mod. When deselected will export as a genshin mod.",)
class CUSTOM_OT_scriptselector(Operator, ExportHelper):
    """Operator to select a script"""
    bl_idname = "script_list.scriptselector"
    bl_label = "Select Script"
    bl_description = "Select a script to run"
    bl_options = {'REGISTER'}
    filename_ext = ".py"
    filter_glob: StringProperty(default="*.py", options={'HIDDEN'},)
    arguments: StringProperty(name="Arguments",
                            description="Arguments to pass to the script", default="", maxlen=1024,)

    def execute(self, context):
        scn = context.scene
        item = scn.script_list.add()
        item.name = self.properties.filepath
        item.arguments = self.properties.arguments
        item.obj_type = context.object.type
        item.obj_id = len(scn.script_list)
        scn.script_index = len(scn.script_list)-1
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "arguments")
class CUSTOM_OT_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "script_list.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.script_index

        try:
            item = scn.script_list[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.script_list) - 1:
                scn.script_list.move(idx, idx+1)
                scn.script_index += 1

            elif self.action == 'UP' and idx >= 1:
                scn.script_list.move(idx, idx-1)
                scn.script_index -= 1

            elif self.action == 'REMOVE':
                scn.script_index -= 1
                scn.script_list.remove(idx)

        if self.action == 'ADD':
            bpy.ops.script_list.scriptselector('INVOKE_DEFAULT')
        return {"FINISHED"}
class MY_PT_SelectStuffPanel(MainPanel, bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "MY_PT_SelectStuffPanel"
    bl_label = "Select Stuff Here you dummy :3"

    def draw_header(self, context: Context):
        layout = self.layout
        row = layout.row()
        row.operator("wm.url_open", text="",icon="QUESTION"
                    ).url = "github.com/leotorrez/LeoTools/blob/main/guides/JoinMeshesGuide.md"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        my_tool = context.scene.my_tool
        split = layout.split(factor=0.75)
        col_1 = split.column()
        col_2 = split.column()
        col_1.prop(my_tool, "ExportFile")
        col_1.prop(my_tool, "OutputFile")
        col_2.operator("export.selector", icon="FILE_FOLDER", text="")
        col_2.operator("output.selector", icon="FILE_FOLDER", text="")
        layout.separator()
        row = layout.row()
        if obj.progress:
            progress_bar = layout.row()
            progress_bar.prop(bpy.context.object,"progress")
            progress_lbl = layout.row()
            progress_lbl.active = False
            progress_lbl.label(text=bpy.context.object.progress_label)
        else:
            if IS_SRMI is True:
                row.prop(my_tool, "star_rail")
                row = layout.row()
            row.operator("my.exportanimation", text="Export Animation")
            row.operator_context = "INVOKE_DEFAULT"
            row.operator("my.execute_auxclass", text="Export Mod")
        # ---------------------------------- SCRIPTS PANEL ----------------------------------
        row = layout.row()
        row.label(text="Scripts for post-processing:")
        row = layout.row()
        rows = 2
        row.template_list("CUSTOM_UL_items", "", scene, "script_list", scene,
                          "script_index", rows=rows)
        col = row.column(align=True)
        col.operator("script_list.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("script_list.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("script_list.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("script_list.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
        row = layout.row()
        row.operator("wm.executescriptbatch", text="Run Scripts in Output Folder")
class OutputFileSelector(bpy.types.Operator, ExportHelper):
    """Export single mod based on current frame"""
    bl_idname = "output.selector"
    bl_label = "Destination"
    filename_ext = "."
    use_filter_folder = True
    filter_glob : bpy.props.StringProperty(default='.', options={'HIDDEN'},)

    def execute(self, context):
        userpath = self.properties.filepath
        if not os.path.isdir(userpath):
            userpath = os.path.dirname(userpath)
            self.properties.filepath = userpath
            userpath = userpath+"\\"
            if not os.path.isdir(userpath):
                msg = "Please select a directory not a file\n" + userpath
                self.report({'ERROR'}, msg)
                return {'CANCELLED'}
        self.properties.filepath = userpath
        context.scene.my_tool.OutputFile = self.properties.filepath
        bpy.ops.ed.undo_push(message="Join Meshes: output selected")
        return{'FINISHED'}
class WMFileSelector(bpy.types.Operator, ExportHelper):
    """Export single mod based on current frame"""
    bl_idname = "export.selector"
    bl_label = "Destination"
    filename_ext = "."
    use_filter_folder = True
    filter_glob : bpy.props.StringProperty(default='.', options={'HIDDEN'},)
    use_foldername : bpy.props.BoolProperty(name="Use foldername when exporting",
        description='''Sets the export name equal to the foldername you are exporting to.
                    Keep true unless you have changed the names''',
        default=True,)
    ignore_hidden : bpy.props.BoolProperty(name="Ignore hidden objects", default=True,
        description="Does not use objects in the Blender window that are hidden while exporting mods",)
    only_selected : bpy.props.BoolProperty(name="Only export selected", default=False,
        description="Uses only the selected objects when deciding which meshes to export",
        )
    no_ramps : bpy.props.BoolProperty(name="Ignore shadow ramps/metal maps/diffuse guide", default=False,
        description="Skips exporting shadow ramps, metal maps and diffuse guides",)
    delete_intermediate : bpy.props.BoolProperty(name="Delete intermediate files", default=False,
        description="Deletes the intermediate vb/ib files after a successful export to reduce clutter",)
    credit : bpy.props.StringProperty(name="Credit",default='',
        description='''Name that pops up on screen when mod is loaded.
                    If left blank, will result in no pop up''',)
    outline_optimization : bpy.props.BoolProperty(name="Outline Optimization",default=False,
        description='''Recalculate outlines. Recommended for final export.
        Check more options below to improve quality''',)
    toggle_rounding_outline : bpy.props.BoolProperty(name="Round vertex positions",default=True,
        description="Rounding of vertex positions to specify which are the overlapping vertices",)
    decimal_rounding_outline : bpy.props.IntProperty(name="Decimals:", default=3,
        description="Rounding of vertex positions to specify which are the overlapping vertices",)
    angle_weighted : bpy.props.BoolProperty(name="Weight by angle",default=False,
        description="Calculate angles to improve accuracy of outlines",)
    overlapping_faces : bpy.props.BoolProperty(name="Ignore overlapping faces",default=False,
        description="Detect and ignore overlapping faces to avoid buggy outlines. Recommended if you have overlaps",)
    detect_edges : bpy.props.BoolProperty(name="Calculate edges",default=False,
        description="Calculate for disconnected edges when rounding, closing holes in the edge outline. Slow",)
    calculate_all_faces : bpy.props.BoolProperty(name="Calculate outline for all faces",
                                                 default=False,
        description='''If you have any flat shaded internal faces or if you just need to fix outline for all faces,
          turn on this option for better outlines. Slow''',)
    nearest_edge_distance : bpy.props.FloatProperty(name="Distance:", default=0.001,
                                                    soft_min=0, precision=4,
        description="Expand grouping for edge vertices within this radial distance to close holes in the edge outline. Requires rounding",)

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
            col.prop(self, 'toggle_rounding_outline', text='Vertex Position Rounding',
                     toggle=True, icon="SHADING_WIRE")
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
            userpath = os.path.dirname(userpath)
            self.properties.filepath = userpath
            userpath = userpath+"\\"
            if not os.path.isdir(userpath):
                msg = "Please select a directory not a file\n" + userpath
                self.report({'ERROR'}, msg)
                return {'CANCELLED'}
        self.properties.filepath = userpath
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
        bpy.ops.ed.undo_push(message="Join Meshes: dump selected")
        return{'FINISHED'}
class ExecuteAuxClassOperator(bpy.types.Operator):
    """Export operation base class"""
    bl_idname = "my.execute_auxclass"
    bl_label = "Export Mod Aux"
    bl_description = "Export mod as a single mesh"
    bl_options = {'REGISTER'}
    operations = []
    def __init__(self):
        self.step = 0
        self.timer = None
        self.done = False
        self.max_step = None
        self.timer_count = 0

    def modal(self, context, event):
        if not self.done:
            context.object.progress = ((self.step+1)/(self.max_step))*100 - 1
            if context.object.progress < 0:
                context.object.progress = 0
            context.object.progress_label = self.operations[self.step]['label']
            context.area.tag_redraw()

        #by running a timer at the same time of our modal operator
        #we are guaranteed that update is done correctly in the interface
        if event.type == 'TIMER':
            #but wee need a little time off between timers to ensure that blender
            #have time to breath, so we have updated inteface
            self.timer_count +=1
            if self.timer_count==10:
                self.timer_count=0
                if self.done:
                    self.step = 0
                    context.object.progress = 0
                    context.window_manager.event_timer_remove(self.timer)
                    context.area.tag_redraw()
                    return {'FINISHED'}
                if self.step < self.max_step:
                    self.operations[self.step]['func'](*self.operations[self.step]['args'])
                    self.step += 1
                    if self.step==self.max_step:
                        self.done=True
                    return {'RUNNING_MODAL'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.operations = []
        self.operations.append(
            {'label': "Exporting...", 'func': self.exporting_process, 'args': (context,)})
        if self.max_step is None:
            self.max_step = len(self.operations)
        context.window_manager.modal_handler_add(self)
        self.timer = context.window_manager.event_timer_add(0.1, window=context.window)
        return {'RUNNING_MODAL'}

    def exporting_process(self, context):
        '''Second process to export mod'''
        try:
            if context.active_object.mode != "OBJECT":
                self.report({'ERROR'}, "Please change to object mode before running")
                return {'CANCELLED'}
            self.exportframe(context, None)
            my_tool = context.scene.my_tool
            if my_tool.OutputFile != "":
                src = os.path.dirname(my_tool.ExportFile) + "Mod"
                dest = os.path.dirname(my_tool.OutputFile) +"\\"+ src.split("\\")[-1]
                self.move_folder_to(src, dest)
                self.report({'INFO'}, f"Mod moved to {dest}")
        except Exception as e:
            self.report({'ERROR'}, f"Error exporting mod: {e}")
            return {'CANCELLED'}
        else:
            self.report({'INFO'}, "Mod exported successfully!!!")
            return {'FINISHED'}

    def exportframe(self, context, filename):
        '''Export the current frame as a mod'''
        scene = context.scene
        my_tool = scene.my_tool
        dir_path = os.path.dirname(my_tool.ExportFile)
        object_name = os.path.basename(dir_path)
        try:
            mainobjects = [obj.name for obj in scene.objects
                           if obj.name.lower().startswith(object_name.lower())
                           and obj.visible_get() and obj.type == "MESH"]
            collectionstojoin = {}
            for col in bpy.data.collections:
                for obj in mainobjects:
                    if obj.lower().startswith(col.name.lower()):
                        collectionstojoin[obj] = col.name
            for obj in mainobjects:
                for key, col in collectionstojoin.items():
                    if obj in bpy.data.collections[col].objects:
                        self.report({"ERROR"}, f"Container {obj} is in collection {col}. This can cause unpredictable results. Please remove it from the collection before continuing.")
                        return {'CANCELLED'}

            # Make Single use everything to avoid linked data issues
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.make_single_user(type='ALL', object=True, obdata=True,
                                            animation=True, obdata_animation=True)

            topop = []
            for obj, col in collectionstojoin.items():
                if self.is_collection_empty(bpy.data.collections[col]):
                    print(f"Collection {col} is empty, skipping")
                else:
                    self.join_into(context, bpy.data.collections[col], obj)
                topop.append(obj)

            for obj in topop:
                collectionstojoin.pop(obj)
                mainobjects.remove(obj)

            if len(mainobjects) > 0:
                print("Warning: some objects were ignored. or had no match.")
                print("Objects ignored: ")
                for obj in mainobjects:
                    print(obj)
            if len(collectionstojoin) > 0:
                print("Warning: some collections were ignored. or had no match.")
                print("Collections ignored: ")
                for col, obj in collectionstojoin.items():
                    print(f"{col} ->{obj}")

            filepath = dir_path + "/" + object_name + ".vb"
            if filename is not None:
                path=dir_path
                filepath = path +"/"+ filename
            vb_path = filepath
            ib_path = os.path.splitext(vb_path)[0] + '.ib'
            fmt_path = os.path.splitext(vb_path)[0] + '.fmt'
            outline_properties = (my_tool.outline_optimization, my_tool.toggle_rounding_outline,
                                my_tool.decimal_rounding_outline, my_tool.angle_weighted,
                                my_tool.overlapping_faces, my_tool.detect_edges,
                                my_tool.calculate_all_faces, my_tool.nearest_edge_distance)
            if IS_SRMI is True:
                export_3dmigoto_genshin(self, bpy.context, object_name, vb_path, ib_path,
                                        fmt_path, my_tool.use_foldername,
                                        my_tool.ignore_hidden, my_tool.only_selected,
                                        my_tool.no_ramps, my_tool.delete_intermediate,
                                        my_tool.credit, outline_properties,
                                        star_rail=my_tool.star_rail)
            else:
                export_3dmigoto_genshin(self, bpy.context, object_name, vb_path, ib_path,
                                        fmt_path, my_tool.use_foldername,
                                        my_tool.ignore_hidden, my_tool.only_selected,
                                        my_tool.no_ramps, my_tool.delete_intermediate,
                                        my_tool.credit, outline_properties)
        except Exception as e:
            self.report({'ERROR'}, f"Error exporting frame: {e}")
        finally:
            bpy.ops.ed.undo_push(message="Join Meshes: frame export")
            bpy.ops.ed.undo()

    def move_folder_to(self, src, dest):
        '''Move a folder to another location'''
        src_file = ""
        dest_file = ""
        try:
            print(f"Moving files to {dest}")
            shutil.copytree(src, dest, dirs_exist_ok=True)
            shutil.rmtree(src)
        except Exception as e:
            self.report({'ERROR'}, f"Error moving file {src_file} to {dest_file}. Error: {e}")
            return {'CANCELLED'}

    def appendto(self, collection, destination):
        '''Append all meshes in a collection to a list'''
        for a_collection in collection.children:
            self.appendto(a_collection, destination)
        for obj in collection.objects:
            if obj.type == "MESH":
                destination.append(obj)

    def join_into(self, context, collection_name, obj,):
        '''Join all meshes in a collection into a single mesh'''
        target_obj = bpy.data.objects[obj]
        objects_to_join = []
        if collection_name is not None:
            self.appendto(bpy.data.collections[collection_name.name], objects_to_join)
        objects_to_join = [obj for obj in objects_to_join 
                           if obj.type == "MESH" and obj.visible_get()]
        objs = objects_to_join
        objs.append(target_obj)

        # apply shapekeys
        for ob in objs:
            ob.hide_viewport = False  # should be visible
            if ob.data.shape_keys:
                ob.shape_key_add(name='CombinedKeys', from_mix=True)
                for shape_key in ob.data.shape_keys.key_blocks:
                    ob.shape_key_remove(shape_key)

        # apply modifiers
        for obj in objs:
            with context.temp_override(active_object=obj, selected_editable_objects=[obj]):
                for modifier in obj.modifiers:
                    if not modifier.show_viewport:
                        obj.modifiers.remove(modifier)
                    else:
                        bpy.ops.object.modifier_apply(modifier=modifier.name)

        # join stuff
        with context.temp_override(active_object=target_obj, selected_editable_objects=objs):
            bpy.ops.object.join()

        # Remove all vertex groups with the word MASK on them
        vgs = [vg for vg in target_obj.vertex_groups if vg.name.find("MASK") != -1]
        if len(vgs) > 0:
            print("Removing vertex groups with MASK in their name:")
            for vg in vgs:
                print(vg.name)
                target_obj.vertex_groups.remove(vg.pop())

    def is_collection_empty(self, collection):
        '''Check if a collection is empty'''
        for obj in collection.objects:
            if obj.type == "MESH" and obj.visible_get():
                return False
        return True
class ExportAnimationOperator(ExecuteAuxClassOperator):
    """Export animation as a mod"""
    bl_idname = "my.exportanimation"
    bl_label = "Export Animation"
    bl_description = "Export animation as a mod"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        scene = context.scene
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        total = frame_end - frame_start + 1
        self.operations = []
        for f in range(frame_start, frame_end + 1):
            self.operations.append(
                {'label': f"Exporting frame {f}/{total}", 'func': self.frame, 'args': (context, f, total)})
        if context.active_object.mode != "OBJECT":
            self.report({'ERROR'}, "Please change to object mode before running")
            return {'CANCELLED'}
        if self.max_step is None:
            self.max_step = len(self.operations)
        print("Starting animation exporting Loop")
        self.report({'INFO'}, f"Frames exported 0/{total}")
        context.window_manager.modal_handler_add(self)
        self.timer = context.window_manager.event_timer_add(0.1, window=context.window)
        return {'RUNNING_MODAL'}

    def frame(self, context, f, total):
        '''Export the current frame as a mod'''
        try:
            scene = context.scene
            export_file = scene.my_tool.ExportFile
            output_file = scene.my_tool.OutputFile
            dir_path = os.path.dirname(export_file)
            object_name = os.path.basename(os.path.dirname(export_file))
            dirname = dir_path + "Mod"
            filename = f"{object_name}f{f:04d}.vb"
            if output_file != "":
                new = f"{output_file}{object_name}f{f:04d}Mod"
            else:
                new = f"{dirname}f{f:04d}"
            scene.frame_set(f)
            self.exportframe(context, filename)
            self.move_folder_to(dirname, new)
            print(f"Mod moved to {new} {f}/{total}")
            self.report({'INFO'}, f"Frame {f}/{total} exported")
        except Exception as e:
            self.report({'ERROR'}, f"Error exporting frame {f}. Error: {e}")
            return {'CANCELLED'}
class CUSTOM_UL_items(UIList):
    '''Custom UIList'''
    def draw_item(self, context, layout, data, item, icon, active_data,
                active_propname, index):
        split = layout.split(factor=0.025)
        split.label(text=f"{index+1}")
        custom_icon = "FILE_SCRIPT"
        split.label(text=item.name, icon=custom_icon)
        split.label(text=item.arguments)

    def invoke(self, context, event):
        '''Invoke the UIList'''
        pass
class MY_OT_ExecuteScriptBatchOperator(Operator):
    """Operator to execute the scripts in my_tool.script_list using dump folder as cwd"""
    bl_idname = "wm.executescriptbatch"
    bl_label = "Execute Scripts"
    bl_description = "Execute the scripts in my_tool.script_list using dump folder as cwd"
    bl_options = {'REGISTER'}
    finished = False

    def modal(self, context, event):
        if self.finished:
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.finished = False
        script_thread = Timer(0,self.script_processing,())
        script_thread.start()
        # script_thread.join()
        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        bpy.ops.wm.executescriptbatch('INVOKE_DEFAULT')

    def script_processing(self):
        '''Second process to run the scripts'''
        scn = bpy.context.scene
        my_tool = scn.my_tool
        cwd = my_tool.OutputFile
        if cwd == '' or not os.path.isdir(cwd):
            cwd = f"{os.path.dirname(my_tool.ExportFile)}Mod"

        total = len(scn.script_list)
        scripts_ran = 0
        for item in scn.script_list:
            args = re.split(r'(--\w+|-\w)', item.arguments)
            res = []
            for i in range(1, len(args), 2):
                res.append(args[i] +' '+ args[i+1].strip())
            args = [arg.strip() for arg in res]
            print(f"Current working directory: {cwd}")
            try:
                print(f"Running {item.name} with arguments {args}")
                # might need to use py or python3 sometimes :fallenqiqi:
                file_process = subprocess.Popen(["python", item.name] + args,
                                                stdin=subprocess.PIPE, cwd=cwd)
                file_process.communicate(input=b"\n")
                file_process.wait()
                stderr = file_process.communicate()[1]
                if stderr:
                    raise Exception(stderr.decode())
                scripts_ran += 1
                self.report({'INFO'},
                            f"({scripts_ran}/{total})Script {item.name} executed successfully")
            except Exception as e:
                self.report({'ERROR'},
                            f"Error running {item.name}. Check console for more information({e})")
                return {'CANCELLED'}
        self.finished = True
        self.report({'INFO'}, "ALL Scripts executed successfully!!!")
        return {'FINISHED'}

classes = (CUSTOM_objectCollection, CUSTOM_OT_scriptselector,
        CUSTOM_OT_actions, MyProperties,
        MY_PT_SelectStuffPanel, ExecuteAuxClassOperator,
        MY_OT_ExecuteScriptBatchOperator, WMFileSelector,
        ExportAnimationOperator, OutputFileSelector, CUSTOM_UL_items)

def register():
    '''Register all classes'''
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)
    bpy.types.Scene.script_list = bpy.props.CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.script_index = IntProperty(name="Index for script_list",
                                               default=0, min=0, max=1000)
    bpy.types.Object.progress = bpy.props.FloatProperty(name="Progress", subtype="PERCENTAGE",
                                                    soft_min=0, soft_max=100, precision=0,)
    bpy.types.Object.progress_label = bpy.props.StringProperty()

def unregister():
    '''Unregister all classes'''
    del bpy.types.Object.progress_label
    del bpy.types.Object.progress
    del bpy.types.Scene.my_tool
    del bpy.types.Scene.script_list
    del bpy.types.Scene.script_index
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
