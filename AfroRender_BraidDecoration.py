import bpy
from math import degrees, floor
import pdb
import numpy as np
from mathutils import Vector


class AfroRender_BraidDecorations(bpy.types.Operator):
    bl_idname = "object.braid_decoration"
    bl_label = "Add Beads or Rings to Braids/Dreads"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    num_ps = len(bpy.context.object.particle_systems) - 1
    beading_patterns = bpy.props.EnumProperty(
                                name = "Bead Patterns",
                                default = "0",
                                description = "Distributing Beads" ,
                                items = [
                                    ("0", "Random", "Randomly distribute beads", 0),
                                    ("1", "Stacks", "Distribute beads at the bottom of each braid", 1),
                                    ("2", "Rings", "Overhanging Rings", 2),
                                    ]
                            )
    bead_name = bpy.props.StringProperty(name = "Bead Object Name", description = "Insert the name of the object to be distributed along the braids", default = "Bead_1") 
    particle_system_index = bpy.props.IntProperty(name = "Particle System Index", description = "Index of Particle System to distribute Beads on", min = 0, max = num_ps, default = 0)
    def execute(self, context): 
        
        bpy.data.objects[self.bead_name].select = True
        target = context.object
        
        if(target.particle_systems == False):
            print("No particle system on this object.")
            return {'FINISHED'}

        ps = target.particle_systems[self.particle_system_index]
        






        return {'FINISHED'}



class AfroRender_BraidDecoPanel(bpy.types.Panel):
    bl_label = "Hair Decoration"
    bl_space_type = 'PROPERTIES'
    bl_idname = "OBJECT_PT_hello" 
    bl_region_type = 'WINDOW'
    bl_context = "particle"

    def draw(self, context):

        layout = self.layout
        Beads = layout.row()
        Beads.operator("object.braid_decoration", text = "Add Beads at Random Points")




def register():
    bpy.utils.register_class(AfroRender_BraidDecorations)
    bpy.utils.register_class(AfroRender_BraidDecoPanel)

register()
