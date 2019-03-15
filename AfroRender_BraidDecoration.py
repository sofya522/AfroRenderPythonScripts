import bpy
from math import degrees, floor
import pdb
import numpy as np
from mathutils import Vector


def stack_beads(ps, context, amplitude):
    print("stacking beads...")
    #make sure the number of keys in each strand is at least 50. 
    #for each hair strand get the keys. 
    #for every key with index greater than num_beads_on_each_braid(user-specified) 
    #place bead at key with size dimension (x,y,z) proportional to braid amplitude 

    #side note: if the beads don't appear as together as you would like, try increasing the number of keys
    #don't forget to orient the beads in the direction of the hair strand

def distribute_beads(ps, context, amplitude):
    print("distributing beads...")
    #not all braids have beads or rings. 
    #on a strand that does have beads or rings, they are not stacked. they are placed randomly and sparsely. 
    #for the number of beads to be distributed:
    #get a random number between 0 and the number of hairs 
    #on that strand, for the number of beads per strand place a bead or ring at random key 

def cornrow_rings(ps, context, amplitude):
    print("adding cornrow rings")
    #every ring should be hanging off at a hair key. dimensions still determined by braid amplitude. 
    #Addition --> check if the braid is actually a cornrow. 

def check_name(name):
    for obj in bpy.data.objects: 
        if name == obj.name:
            return True 

    return False


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
        
        if(check_name(self.bead_name) == False):
            print("Please enter the correct name of the bead or ring.")
            return {'FINISHED'}
        
        else:
            bpy.data.objects[self.bead_name].select = True
            
        
        target = context.object
        
        if(target.particle_systems == False):
            print("No particle system on this object.")
            return {'FINISHED'}

        ps = target.particle_systems[self.particle_system_index]
        print(ps.settings.kink)
        if(ps.settings.kink != 'BRAID'):
            print("Please create an adequate braiding or dreadlock groom before proceeding.")
            return {'FINISHED'}

        amp = ps.settings.kink_amplitude
        freq = ps.settings.kink_frequency
        num_segments = ps.settings.hair_step

        
        hairs = ps.particles
        for i, h in enumerate(hairs): 
            print('hair number {i}:'.format(i=i))
            for i, hv in enumerate(h.hair_keys):
                print('  vertex {i} coordinates: {co}'.format(i=i, co=hv.co))


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
