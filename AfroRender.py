import bpy
import math

#boolean for if the artist wants to use a curve widget rather than buttons 
widget_boolean = False 
bpy.types.Scene.use_widget = bpy.props.BoolProperty(name = "Use Widget", description = "Use the Curve Widget to get Hair StrandFrequency/Amplitude", default = False)
#Hair Chart - Maps all types of hair to menu that the user can see 
global_afro_count = 0 
def count_Afros(context):
    if(context.object.particle_systems == False):
        return 0; 
    
    else:

        Afro_num = 0; 
        for ps in range (len(context.object.particle_systems)):
            if "Afro" in context.object.particle_systems[ps].name:
                Afro_num += 1; 

        global_afro_count = Afro_num
        if(global_afro_count == 0):
            return len(context.object.particle_systems)

        return Afro_num 
    return 0; 

def get_Afro(ps):

    if ps.settings.use_advanced_hair != True:
            ps.settings.use_advanced_hair = True
            ps.settings.factor_random = 0.3

    ps.settings.type = 'HAIR'
    ps.settings.child_type = 'SIMPLE'
    ps.settings.draw_step = 9
    ps.settings.render_step = 9
    ps.settings.hair_step = 50; 
    ps.settings.kink = 'CURL'
    ps.settings.kink_frequency = 30
    ps.settings.kink_amplitude = 0.04
    ps.settings.count = 100
    ps.settings.hair_length = 0.3
        #randomness
    ps.settings.roughness_2 = 0.2
    ps.settings.roughness_1 = 0.1
    ps.settings.roughness_2_size = 1.0
    ps.settings.roughness_endpoint = 0.2
    ps.settings.roughness_end_shape = 1.0
    ps.settings.rendered_child_count = 50 

    ps.settings.use_clump_curve = True 
    clump_hair(ps.settings.clump_curve.curves[0], False)


def get_sidehair(ps):
    ps.settings.type = 'HAIR'
    ps.settings.child_type = 'SIMPLE'
    ps.settings.draw_step = 7
    ps.settings.render_step = 7
    ps.settings.hair_step = 10; 
    ps.settings.kink = 'WAVE'
    ps.settings.kink_frequency = 5
    ps.settings.kink_amplitude = 0.02
    ps.settings.count = 0
    ps.settings.hair_length = 0.8
    ps.settings.roughness_2 = 0.0
    ps.settings.roughness_1 = 0.1
    ps.settings.roughness_2_size = 1.0
    ps.settings.roughness_endpoint = 0.4
    ps.settings.roughness_end_shape = 1.0
    ps.settings.rendered_child_count = 100
    

def get_box_braids(ps):
    ps.settings.type = 'HAIR'
    ps.settings.child_type = 'SIMPLE'
    ps.settings.draw_step = 10
    ps.settings.render_step = 10
    ps.settings.hair_step = 50; 
    ps.settings.kink = 'BRAID'
    
    ps.settings.kink_amplitude = 0.01
    ps.settings.count = 0
    ps.settings.hair_length = 0.8
    length = ps.settings.hair_length
    ps.settings.kink_frequency = int(math.ceil(length)) * 30
 

    ps.settings.roughness_2 = 0.01
    ps.settings.roughness_1 = 0.0
    ps.settings.roughness_2_size = 0.1
    ps.settings.roughness_endpoint = 0.0
    ps.settings.roughness_end_shape = 1.0
    ps.settings.child_nbr = 100 
    ps.settings.rendered_child_count = 100
    ps.settings.use_clump_curve = True 
    clump_hair(ps.settings.clump_curve.curves[0], True)

#Creates a particle system if one doesn't already exist 
def get_particle_system(context, edges, box_braids):  
    
    print("This object already has a particle system")
    #print(context.object.particle_systems[0].name)

    Afro_count = count_Afros(context)
    print(Afro_count)
    new_ps_name = "Afro %d" % Afro_count
    print(new_ps_name)

    bpy.ops.object.particle_system_add()
    ps = context.object.particle_systems[Afro_count]
    ps.name = new_ps_name
    if(edges):
        get_sidehair(ps)
    elif(box_braids):
        get_box_braids(ps)
    else:
        get_Afro(ps)

        
def clump_hair(clump_curve, box_braids):

    if(box_braids):
        clump_curve.points[0].location.x = 0.0
        clump_curve.points[0].location.y = 0.5
        clump_curve.points[1].location.x = 1.0
        clump_curve.points[1].location.y = 1.0


    else:
        clump_curve.points[0].location.x = 0.0
        clump_curve.points[0].location.y = 0.0
        clump_curve.points[1].location.x = 1.0
        clump_curve.points[1].location.y = 1.0


#creates a new nodegroup for the curve widget interactive UI element 
def make_node_group(name):
    if 'frq_amp' not in bpy.data.node_groups:
            new_curve_widget = bpy.data.node_groups.new('frq_amp', 'ShaderNodeTree')
            new_curve_widget.fake_user = True 


#add and initialize a Shader Node RGB Curve to node group (only used for hair mapping, not RGB values)
all_nodes={}
def get_node(name):

    group = bpy.data.node_groups[0].nodes
    if name not in all_nodes:
        new_node = group.new('ShaderNodeRGBCurve')
        all_nodes[name] = new_node.name

    group[all_nodes[name]].mapping.initialize()
    return group[all_nodes[name]] 

#Hair Charting Function - Maps user input to value inputs for curl frequency and amplitude 
def create_hair_type(hair_chart, context):
    global_afro_count = count_Afros(context)
    print("Global AfroCount:")
    print(global_afro_count)
    print("Num PS:")
    print(len(bpy.context.object.particle_systems))
    ps = bpy.context.object.particle_systems[global_afro_count - 1]
    
    if hair_chart == "0":
        print("2A")
        ps.settings.kink_frequency = 1
        ps.settings.kink_amplitude = 0.04
        
    elif hair_chart == "1":
        print("2B")
        ps.settings.kink_frequency = 10
        ps.settings.kink_amplitude = 0.04
        
    elif hair_chart == "2":
        print ("2C")
        ps.settings.kink_frequency = 10
        ps.settings.kink_amplitude = 0.1
        
    elif hair_chart == "3":
        print ("3A")
        ps.settings.kink_frequency = 9
        ps.settings.kink_amplitude = 0.25
        
    elif hair_chart == "4":
        print ("3B")
        ps.settings.kink_frequency = 15
        ps.settings.kink_amplitude = 0.15
        
    elif hair_chart == "5":
        print ("3C")
        ps.settings.kink_frequency = 25
        ps.settings.kink_amplitude = 0.08
        
    elif hair_chart == "6":
        print("4A")
        ps.settings.kink_frequency = 40
        ps.settings.kink_amplitude = 0.08
        
    elif hair_chart == "7":
        print ("4B")
        ps.settings.kink_frequency = 80
        ps.settings.kink_amplitude = 0.05
        
    elif hair_chart == "8":
        print ("4C")
        ps.settings.kink_frequency = 50
        ps.settings.kink_amplitude = 0.03 
    
#creates UI for AfroRender 
class AfroRenderPanel (bpy.types.Panel):
    """Display Hair Type Choices"""
    
    bl_label = "AfroRender"
    bl_space_type = 'PROPERTIES'
    bl_idname = "OBJECT_PT_hello" 
    bl_region_type = 'WINDOW'
    bl_context = "particle"

    def draw(self, context):
        layout = self.layout
        NaturalHair = layout.row()
        NaturalHair.operator("object.natural_hair", text = "Create Afro")

        Edges = layout.row()
        Edges.operator("object.make_edges", text = "Create Side Hairs or Edges")

        # chart_row = layout.row(align =True)
        # chart_row.prop(context.scene, 'hair_chart', expand = True)    

        scene = bpy.data.scenes["Scene"]
        row = layout.row(align=True)
        row.prop(context.scene, "use_widget")
        
        if scene.use_widget == True: 
            make_node_group('frq_amp')
            node = get_node('frq_amp_curve')
            self.layout.template_curve_mapping(node, "mapping")
            row = layout.row()
            row.operator("object.hair_curve", text="Widget Control")
            
        Braids = layout.row()
        Braids.operator("object.braids", text = "Create Box Braids")

def get_frizz (frizz_val, uniform_val, clump_val, thickness, context):
    print ("Create Frizziness")
    global_afro_count = count_Afros(context)
    ps = bpy.context.object.particle_systems[global_afro_count - 1].settings
    if (frizz_val > 0):

        
        ps.roughness_2 += frizz_val  + 0.5
        ps.roughness_2_size +=  frizz_val 
        ps.roughness_1 += frizz_val  
        ps.roughness_endpoint += frizz_val / 2
        ps.roughness_2_size -= frizz_val  
    
    elif (frizz_val < 0): 
        ps.roughness_2 -= frizz_val  + 1 
        ps.roughness_2_size -=  frizz_val 
        ps.roughness_1 -= frizz_val  
        ps.roughness_endpoint -= frizz_val / 2
        ps.roughness_2_size += frizz_val  

    if (uniform_val > 0) : 
        ps.factor_random = uniform_val
        ps.roughness_endpoint = uniform_val / 2.0 
    
    if(clump_val > 0):
        ps.clump_factor = 1.0
        ps.clump_shape = 0.5

    if(thickness > 0): 
        ps.count = thickness * 1000



def get_simulation(context, hair_chart):
    global_afro_count = count_Afros(context)
    ps = bpy.context.object.particle_systems[global_afro_count - 1]
    #hair_chart = int(hair_chart)
    print(hair_chart[0])
    print("Computing Simulation Parameters...") 
    ps.use_hair_dynamics = True 
    ps.settings.child_nbr = 4
    sim_settings = ps.cloth.settings
    sim_settings.quality = 50;
    ps.settings.render_type = 'PATH'
    #stiffness= ps.cloth.settings.bending_stiffness
    

    if(hair_chart == "0" or hair_chart == "1" or hair_chart == "2"):
        sim_settings.bending_stiffness = 0.38
        #sim_settings.bending_damping = 0.7
        #sim_settings.pin_stiffness = 0.1
        sim_settings.mass = 0.3

    elif (hair_chart == "3" or hair_chart == "4" or hair_chart == "5"):
        sim_settings.bending_stiffness = 0.5
        sim_settings.bending_damping = 0.9
        sim_settings.pin_stiffness = 0.5
        sim_settings.mass = 0.2
        print("second iteration")

    elif (hair_chart == "6" or hair_chart == "7" or hair_chart == "8"):
        sim_settings.bending_stiffness = 1
        sim_settings.pin_stiffness = 1
        sim_settings.bending_damping = 1
        sim_settings.mass = 0.1
        print("third iteration")



def get_vertex_group(context, group_ind, edges):
    global_afro_count = count_Afros(context)
    ps = context.object.particle_systems[global_afro_count - 1]
    print("in vertex group function...")
    print(ps.vertex_group_density) 
    if len(context.object.vertex_groups) > 0:
        ps.settings.render_type = 'PATH'
        ps.vertex_group_density = context.object.vertex_groups[group_ind].name


def create_edge_particle_system(context, edge_chart):
    global_afro_count = count_Afros(context)
    ps = bpy.context.object.particle_systems[global_afro_count - 1]
    if edge_chart == "0":
        print("2A")
        ps.settings.kink_frequency = 1
        ps.settings.kink_amplitude = 0.04





class AfroRender_Edges(bpy.types.Operator):

    bl_idname = "object.make_edges"
    bl_label = "Edges" 
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    

    baby_hairs = bpy.props.BoolProperty(name = "Create Baby Hairs", description = "Edges for Baby Hairs", default = False)
    edge_type = bpy.props.EnumProperty(
                                name = "Edge Type",
                                default = "0",
                                description = "Straight or wavy edges" ,
                                items = [
                                    ("0", "Straight Edges (1A)", "Straight Edges", 0),
                                    ("1", "Wavey Edges (4C)", "Wavey Edges", 1),
                                    ]
                            )
    use_v_groups = bpy.props.BoolProperty(name = "Use Vertex Group", description = "Only display edges on specified vertex group", default= True)
    group_num = bpy.props.IntProperty(name = "Vertex Group Index", description = "Whichever Vertex Group Artist wants to Afro-ize", default = 0, min= 0)
    def execute (self, context):
        scene = bpy.data.scenes["Scene"]
        get_particle_system(context, True, False) 
       
        if (self.use_v_groups == True):
            get_vertex_group(context, self.group_num, True) 

        bpy.context.scene.frame_set(0)
        return {'FINISHED'}



#executes hair charting
class AfroRender_NaturalHair(bpy.types.Operator):

    bl_idname = "object.natural_hair"
    bl_label = "Create Natural Hair Particle System"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    #use_widget = bpy.props.BoolProperty(name = "Use Widget", description = "Use the Curve Widget to get Hair StrandFrequency/Amplitude", default = False)

    hair_chart = bpy.props.EnumProperty(
                                name = "Hair Chart",
                                default = "8",
                                description = "Hair Charting" ,
                                items = [
                                    ("0", "2A", "First Iteration of straight hair", 0),
                                    ("1", "2B", "First Iteration of Wavey Hair", 1),
                                    ("2", "2C", "Wavey Hair 2", 2),
                                    ("3", "3A", "First iteration of curly hair", 3),
                                    ("4", "3B", "Curly Hair 2", 4),
                                    ("5", "3C", "Curly Hair 3", 5),
                                    ("6", "4A", "First Iteration of Kinky hair", 6),
                                    ("7", "4B", "kinky hair 2", 7),
                                    ("8", "4C", "kinky hair 3", 8),
                                    ]
                            )

    use_materials = bpy.props.BoolProperty(name = "Use Materials",  description = "Add Natural Hair Shader", default = False)
    use_simulation = bpy.props.BoolProperty(name = "Simulation Presets",  description = "Create Simulated Afro", default = True)
    use_vertex_group = bpy.props.BoolProperty(name = "Use Vertex Group",  description = "Only display Afro on a Specified Vertex Group", default = True)
    group_num = bpy.props.IntProperty(name = "Vertex Group Index", description = "Whichever Vertex Group Artist wants to Afro-ize", default = 0, min= 0)

    frizziness = bpy.props.FloatProperty(name = "Frizziness", description = "Decrease to create promient coils", min = -1.0, max = 1.0, default = 0.0)
    length_uniformity = bpy.props.FloatProperty(name = "Length Uniformity", description = "Increase for less randomness", min = 0.0, max = 1.0, default = 0.25)
    coiliness = bpy.props.FloatProperty(name = "Coiliness", description = "Increase for more adhesive curls", min = 0.0, max = 1.0, default = 0.0)
    thickness = bpy.props.FloatProperty(name = "Thickness", description = "Thickness of the Afro", min = 0.0, max = 1.0, default = 0.5)


    def execute(self, context):
        scene = bpy.data.scenes["Scene"]
        get_particle_system(context, False, False) 
        create_hair_type(self.hair_chart, context)
        get_frizz(self.frizziness, self.length_uniformity, self.coiliness, self.thickness, context)
        
        if(self.use_simulation == True):

            get_simulation(context, self.hair_chart)


        if (self.use_vertex_group == True):
            
            get_vertex_group(context, self.group_num, False) 


        #swidget_boolean = self.use_widget
        bpy.context.scene.frame_set(0)
        print ("natural hair button pressed")
    
        return {'FINISHED'}

#maps curve widget to hair frequency/amplitude parameters 
class AfroRender_CurveWidget(bpy.types.Operator):
    """Correlate Hair and Curve Widget"""
    bl_idname = "object.hair_curve"
    bl_label = "Control Hair Frequency and Amplitude with Curve Widget"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        index = len(bpy.data.node_groups[0].nodes) - 1
        curve_widget = bpy.data.node_groups[0].nodes[index].mapping.curves[3]

        frequency = curve_widget.points[1].location.x
        amplitude = curve_widget.points[1].location.y

        particle_sys = context.object.particle_systems[0]
     
        particle_sys.settings.kink_frequency = frequency * 100 
        particle_sys.settings.kink_amplitude = amplitude / 5

        print(frequency)
        print(amplitude)

        return {'FINISHED'}

class AfroRender_Braiding(bpy.types.Operator):

    bl_idname = "object.braids"
    bl_label = "Create Braided Particle System"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        get_particle_system(context, False, True)

        print ("braided button pressed")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AfroRenderPanel)
    bpy.utils.register_class(AfroRender_NaturalHair)
    bpy.utils.register_class(AfroRender_Braiding)
    bpy.utils.register_class(AfroRender_CurveWidget)
    bpy.utils.register_class(AfroRender_Edges)
        
register()