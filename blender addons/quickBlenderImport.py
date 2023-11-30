# this script helps importing the files contained in a folder and setting them up in the scene for modding workflow
import os
import bpy
from blender_3dmigoto_gimi import Import3DMigotoFrameAnalysis
from blender_dds_addon import import_dds
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "Quick GIMI Import",
    "blender": (2, 80, 0),
    "author": "LeoTorreZ / LeoMods",
    "location": "File > Import-Export",
    "description": "Eases the import and set up process of GIMI dumps.",
    "category": "Import-Export",
    "tracker_url": "https://github.com/leotorrez/LeoTools",
}

# run blender_3dmigoto_gimi to import meshes. prompting user to find it
class QuickImport(Import3DMigotoFrameAnalysis):
    bl_idname = "import_scene.3dmigoto_frame_analysis"
    bl_label = "Quick Import for GIMI"
    bl_options = {"UNDO"}

    def execute(self, context):
        super().execute(context)
        folder = os.path.dirname(self.properties.filepath)
        print("------------------------")
        print("------------------------")
        print("------------------------")

        print(f"Found Folder: {folder}")
        # get all the files in the folder ends in diffuse.dds
        files = os.listdir(folder)
        files = [f for f in files if f.endswith("Diffuse.dds")]
        print(f"List of files:{files}")
        # import all the texture files with the import_dds addon and assign materials to meshes following the following format foldername+materialname
        importedmeshes = import_files(context, files, folder)

        # select all imported meshes, go to edit mode
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        for obj in importedmeshes:
            obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')          

         # Select all vertices and merge by distance with sharpedges=True
        bpy.ops.mesh.select_all(action='SELECT') 
        bpy.ops.mesh.remove_doubles(use_sharp_edge_from_normals=True)

        # Alt + J with all options selected (tris to quads conversion)
        bpy.ops.mesh.tris_convert_to_quads(uvs=True,vcols=True,seam=True,sharp=True,materials=True)

        # Cleanup: Delete loose vertices
        bpy.ops.mesh.delete_loose()
        return {"FINISHED"}

def newMat(name, texture_name):
    """Creates a new material using that texture as base color. also sets alpha to none"""
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (1, 1, 1, 1)
    bsdf.inputs[5].default_value = 0.0
    # add texture
    texImage = material.node_tree.nodes.new("ShaderNodeTexImage")
    # get already imported texture
    texture_name = texture_name[:-4]
    texImage.image = bpy.data.images[texture_name]
    texImage.image.alpha_mode = "NONE"
    # link texture to bsdf
    material.node_tree.links.new(texImage.outputs[0], bsdf.inputs[0])
    return material.name

def import_dafile(context, file):
    """Import a file."""
    dds_options = context.scene.dds_options
    tex = import_dds.load_dds(
        file,
        invert_normals=dds_options.invert_normals,
        cubemap_layout=dds_options.cubemap_layout,
    )
    return tex

def import_files(context: bpy.types.Context, files, path):
    importedmeshes=[]
    for file in files:
        # Extract mesh name from the file name
        mesh_name = bpy.path.display_name_from_filepath(os.path.join(path, file))
        # remove "Diffuse" from end of name
        mesh_name = mesh_name[:-7]

        # Import the file
        import_dafile(context, file=os.path.join(path, file))

        # Create a material for the mesh
        material_name = "mat_" + mesh_name
        mat = newMat(material_name, file)

        # Assign the material to the imported mesh
        # find first mesh that has mesh_name at the start of their name
        for obj in bpy.data.objects:
            print(f"Checking {obj.name} agaist {mesh_name}")
            if obj.name.startswith(mesh_name):
                # append created material
                print(f"FOUND! Assigning material {mat} to {obj.name}")
                obj.data.materials.append(bpy.data.materials[mat])
                importedmeshes.append(obj)
                break
    return importedmeshes

def menu_func_import(self,context):
    self.layout.operator(QuickImport.bl_idname, text="Quick Import for GIMI")

def register():
    register_class(QuickImport)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    unregister_class(QuickImport)

if __name__ == "__main__":
    register()