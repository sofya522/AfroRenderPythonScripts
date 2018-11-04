import bpy

#boolean for if the artist wants to use a curve widget rather than buttons 
bpy.types.Scene.use_widget = bpy.props.BoolProperty(name = "Use Widget", description = "Use the Curve Widget to get Hair StrandFrequency/Amplitude", default = False)

#Hair Chart - Maps all types of hair to menu that the user can see 
bpy.types.Scene.hair_chart = bpy.props.EnumProperty(
                                name = "Hair Chart",
                                default = "0",
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
                
#Creates a particle system if one doesn't already exist 
def get_particle_system(context):
	if(context.object.particle_systems):
		print("This object already has a particle system")
		
	else:
		bpy.ops.object.particle_system_add()
		ps = context.object.particle_systems[0]
		
		if ps.settings.use_advanced_hair != True:
			ps.settings.use_advanced_hair = True
			ps.settings.factor_random = 0.5

		ps.settings.type = 'HAIR'
		ps.settings.child_type = 'INTERPOLATED'
		ps.settings.draw_step = 7
		ps.settings.render_step = 7
		ps.settings.kink = 'CURL'
		ps.settings.kink_frequency = 30
		ps.settings.kink_amplitude = 0.04
		ps.settings.count = 25

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
def create_hair_type(hair_chart):
	ps = bpy.context.object.particle_systems[0]
	
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
		NaturalHair.label(text = "Natural Hair")
		NaturalHair.operator("object.natural_hair", text = "Natural Hair")

		chart_row = layout.row(align =True)
		chart_row.prop(context.scene, 'hair_chart', expand = True)    

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
		Braids.label(text = "Generate Braids")
		Braids.operator("object.braids", text = "Braided Hair")


#executes hair charting
class AfroRender_NaturalHair(bpy.types.Operator):

	bl_idname = "object.natural_hair"
	bl_label = "Create Natural Hair Particle System"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		scene = bpy.data.scenes["Scene"]
		get_particle_system(context) 
		create_hair_type(scene.hair_chart)
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

#coming soon! 
class AfroRender_Braiding(bpy.types.Operator):

	bl_idname = "object.braids"
	bl_label = "Create Braided Particle System"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		print ("braided button pressed")
		return {'FINISHED'}


def register():
	bpy.utils.register_class(AfroRenderPanel)
	bpy.utils.register_class(AfroRender_NaturalHair)
	bpy.utils.register_class(AfroRender_Braiding)
	bpy.utils.register_class(AfroRender_CurveWidget)
		
register()