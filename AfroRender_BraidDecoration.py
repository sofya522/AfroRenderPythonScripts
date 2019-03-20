import bpy
from math import degrees, floor
import pdb
import numpy as np
from mathutils import Vector
import random

#Warning: Tool may be used multiple times but may crash if user tries to undo and use again after undoing operator. If you run into that issue, re-run the script after undoing. 
scene = bpy.context.scene

#Three different beading patterns to choose from:
    #1. Random Distrbution - randomly distributes beads or rings about particle system (call distribute_beads function) 
    #2. Stacked Beads - stack beads at the bottom of each braid (call stack_beads function)
    #3. Cornrow Rings - same thing as random distribution but orients selected ring geometry to be almost perpendicular to braid (call cornrow_rings)
bpy.types.Scene.beading_patterns = bpy.props.EnumProperty(
                                name = "Bead Patterns",
                                default = "1",
                                description = "Distributing Beads" ,
                                items = [
                                    ("0", "Random", "Randomly distribute beads", 0),
                                    ("1", "Stacks", "Distribute beads at the bottom of each braid", 1),
                                    ("2", "Rings", "Overhanging Rings", 2),
                                    ]
                            )
#Name of the bead geometry in hiearchy of all objects in the scene 
bpy.types.Scene.bead_name = bpy.props.StringProperty(name = "Bead Object Name", description = "Insert the name of the object to be distributed along the braids", default = "Bead_1") 
   
#Index of Particle System to add beads to 
bpy.types.Scene.particle_system_index = bpy.props.IntProperty(name = "Particle System Index", description = "Index of Particle System to distribute Beads on", min = 0, max = 5)
   
#Number of beads to distribute. If the user wants to stack beads, this will be the number of beads per stand. Otherwise, it's the total number of beads in the particle system. 
bpy.types.Scene.num_beads = bpy.props.IntProperty(name = "Number of Beads", description = "Input the number of beads you want distributed or stacked per braid", min = 1, max = 100)

#Randomization of Beads or use multiple bead types. 
    #--->With this parameter, this tool will check if there are multiple types of beads. (ie, objects with Bead 1, Bead 2, etc)
    #---> otherwise, if there is only one type of bead, will randomly scale each instance of a bead. 
bpy.types.Scene.randomize_beads = bpy.props.BoolProperty(name = "Randomization of Beads in Stack", description = "If activated, there will be more than 1 type of bead in stack", default = False)

#Method of Duplication - if user has not groomed hairstyle at all, check this as instancing is more efficient than duplicating every bead. 
bpy.types.Scene.use_groups = bpy.props.BoolProperty(name = "Use Groups", description = "If activiated, tool will use instancing of bead stacks instead of duplicating individual beads.", default = False)
#make a group of bead objects. 

def get_hair_dir(particle):
    a = particle.hair_keys[0].co
    b = particle.hair_keys[1].co
    c = - a + b
    d = c/np.sqrt(c[0]**2 + c[1]**2 +c[2]**2 )
    print(d)
    return d

def get_segment_dir(seg_1, seg_2):
    a = seg_1
    b = seg_2
    c = - a + b
    d = c/np.sqrt(c[0]**2 + c[1]**2 +c[2]**2 )
    print(d)
    return d

def bead_grouping(ps, context, num_beads, bead, randomize):
    print("grouping beads...")
    bead.location[0] = 0.0
    bead.location[1] = 0.0
    bead.location[2] = 0.0

    
    bead_group = bpy.data.groups.new("Bead_Stack")
    bead_group.objects.link(bead)
    create_stack(bead, num_beads, bead_group)
    return bead_group

def create_stack(bead_obj, num_beads, bead_group):
    
    offset = bead_obj.dimensions[2]  
    print(offset)
    prev = bead_obj  
    for i in range (0,num_beads):
        new_bead= bead_obj.copy()
        new_bead.data = bead_obj.data.copy()
        new_bead.location = bead_obj.location
        new_bead.location[2] = prev.location[2] +  offset
        scene.objects.link(new_bead)
        bead_group.objects.link(new_bead)
        prev = new_bead

def bead_instancing(context, group, bead, hair, position):
    print("instancing beads...")
    #only_render_in_display()
    
    new_instance = bpy.data.objects.new("Instance", None)
    new_instance.dupli_type = 'GROUP'
    new_instance.dupli_group = group
    new_instance.location = position

    v1 = get_hair_dir(hair) 
    v0 = Vector((0,0,1))
    rot = v0.rotation_difference(v1).to_euler()
    new_instance.rotation_euler = rot 
    scene.objects.link(new_instance)


    print("got through bead instancing function")



def only_render_in_display():
    for area in bpy.context.screen.areas: # iterate through areas in current screen
        if area.type == 'VIEW_3D':
            for space in area.spaces: # iterate through spaces in current VIEW_3D area
                if space.type == 'VIEW_3D': # check if space is a 3D view
                    space.show_only_render = True 

def stack_beads(ps, context, num_beads, bead, randomize):

    bead.select = True 

    if(scene.use_groups == True):  
        group = bead_grouping(ps, context, num_beads, bead, randomize)
    

        amp = ps.settings.kink_amplitude
        print(amp)

        print("stacking beads...")
        if check_hairs(ps) != True:
            print("returning false. ")
            return False 
        hairs = context.object.particle_systems[0].particles
        print(context.object.particle_systems[0].name)
        print(hairs[0].hair_keys[0].co.x)
        for i, h in enumerate(hairs): 
            print('hair number {i}:'.format(i=i))
            num_keys = len(h.hair_keys)
            curr_hair = i
            if(num_keys < 3): 
                print("Not enough keys on this strand.")
                continue 
            prev = h.hair_keys[0].co
            for i, hv in enumerate(h.hair_keys):

                start_index = num_keys - num_beads
                #print(start_index)
                if i == abs(start_index):
                    print("add a bead to the strand at this time")
                 
               # print('  vertex {i} coordinates: {co}'.format(i=i, co=hv.co))
                    bead_instancing(context, group, bead, h, hv.co)
                    prev= hv.co
                
    else: 
        print("not using groups... find another way to get directions right")
        hairs = context.object.particle_systems[0].particles
        strand_length = context.object.particle_systems[0].settings.hair_length 
        bead_length = bead.dimensions[2]
        for i, h in enumerate(hairs): 
            print('hair number {i}:'.format(i=i))
            num_keys = len(h.hair_keys)
            curr_hair = i
            if(num_keys < 3): 
                print("Not enough keys on this strand.")
                continue 
            seg_length = strand_length / num_keys
            print(seg_length)
            prev = h.hair_keys[0].co
            cumulative_length = 0 
            for i, hv in enumerate(h.hair_keys):

                start_index = num_keys - num_beads
                #print(start_index)
                if i >= abs(start_index) and cumulative_length >= bead_length:
                    print("add a bead to the strand at this time")

                    new_bead = bead.copy()
                    new_bead.data = bead.data.copy()

                    new_bead.location = hv.co
                    v1 = get_segment_dir(prev, hv.co)
                    v0 = Vector((0,0,1))
                    rot = v0.rotation_difference(v1).to_euler()
                    new_bead.rotation_euler = rot 
                    scene.objects.link(new_bead)
                    prev = hv.co
                    cumulative_length = 0

                cumulative_length += seg_length 
   
    #make sure the number of keys in each strand is at least 50. 
    #for each hair strand get the keys. 
    #for every key with index greater than num_beads_on_each_braid(user-specified) 
    #place bead at key with size dimension (x,y,z) proportional to braid amplitude 
        #---> For effiency and organization, make sure that instead of just duplicating the bead object a bunch of times, 
        #---> create a group of beads objects and instance them. 
        #---> if the user wants some randomness among beads, create a number of different groups based on amount of randomness or size difference

    #side note: if the beads don't appear as together as you would like, try increasing the number of keys
    #don't forget to orient the beads in the direction of the hair strand

def distribute_beads(ps, context, num_beads, bead):
    print("distributing beads...")
    bead.select = True
    #hairs = context.object.particle_systems[scene.particle_system_index].particles
    hairs = context.object.particle_systems[0].particles
    for i in range(0, num_beads): 
        random_hair = hairs[random.randrange(len(hairs))]
        random_segment = random_hair.hair_keys[random.randrange(len(random_hair.hair_keys) - 1)] 
        new_pos = random_segment.co

        new_bead = bead.copy()
        new_bead.data = bead.data.copy()

        new_bead.location = new_pos
        v1 = get_hair_dir(random_hair)
        v0 = Vector((0,0,1))
        rot = v0.rotation_difference(v1).to_euler()
        new_bead.rotation_euler = rot 
        scene.objects.link(new_bead)



    #not all braids have beads or rings. 
    #on a strand that does have beads or rings, they are not stacked. they are placed randomly and sparsely. 
    #for the number of beads to be distributed:
    #get a random number between 0 and the number of hairs 
    #on that strand, for the number of beads per strand place a bead or ring at random key 

def cornrow_rings(ps, context, num_beads, bead):
    print("adding cornrow rings")
    #every ring should be hanging off at a hair key. dimensions still determined by braid amplitude. 
    #Addition --> check if the braid is actually a cornrow. 

def check_name(name):
    for obj in bpy.data.objects: 
        if name == obj.name:
            return True 

    return False



def check_hairs(ps):
    hairs = ps.particles 
    print (len(hairs))
    if (len(hairs) >= 5):
        return True 

    return False     
#main execution 
class AfroRender_BraidDecorations(bpy.types.Operator):
    bl_idname = "object.braid_decoration"
    bl_label = "Add Beads or Rings to Braids/Dreads"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    
    
    def execute(self, context): 
        
        #checks if the specifed bead object exists 
        if(check_name(scene.bead_name) == False):
            print("Please enter the correct name of the bead or ring.")
            return {'FINISHED'}
        
        else:
            bead_object = bpy.data.objects[scene.bead_name]
            
        #selected object
        target = context.object
        
        #checks if user has created a particle system 
        if(target.particle_systems == False):
            print("No particle system on this object.")
            return {'FINISHED'}

        ps = target.particle_systems[0]
        print(ps.settings.kink)

        #checks if beading is possible with the specified particle system 
        if(ps.settings.kink != 'BRAID'):
            print("Please create an adequate braiding or dreadlock groom before proceeding.")
            return {'FINISHED'}


        amp = ps.settings.kink_amplitude
        freq = ps.settings.kink_frequency
        num_segments = ps.settings.hair_step

        

        if scene.beading_patterns == "1":
            stack_beads(ps, context, scene.num_beads, bead_object, scene.randomize_beads)
        
        elif scene.beading_patterns == "0":
            distribute_beads(ps, context, scene.num_beads, bead_object)
        
        elif scene.beading_patterns == "2":
            cornrow_rings(ps, context, scene.num_beads, bead_object)



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
        Beads.operator("object.braid_decoration", text = "Add Beads")

        row = self.layout.row(align=True)
        row.prop(context.scene,"beading_patterns")

        row = self.layout.row(align=True)
        row.prop(context.scene, "bead_name")

        row = self.layout.row(align=True)
        row.prop(context.scene, "particle_system_index")

        row = self.layout.row(align=True)
        row.prop(context.scene, "num_beads")

        row = self.layout.row(align=True)
        row.prop(context.scene, "randomize_beads")

        row = self.layout.row(align=True)
        row.prop(context.scene, "use_groups")





def register():
    bpy.utils.register_class(AfroRender_BraidDecorations)
    bpy.utils.register_class(AfroRender_BraidDecoPanel)

register()
