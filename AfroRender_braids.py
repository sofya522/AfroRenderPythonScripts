import bpy  
from mathutils import Vector 
from math import sin, cos, pi 
from bpy.props import  (FloatProperty,
                        FloatVectorProperty,
                        IntProperty,
                        BoolProperty,
                        StringProperty)

def count_braids(): 
    num_braids = 0 
    for obj in bpy.data.objects: 
        if "Braid" in obj.name:
            num_braids += 1
    return num_braids

def get_length(context):
    
    obj_name_original = context.active_object.name
    if(check_name(obj_name_original) == False):
        print("You need to activiate an object!") 
        
        return "No Object Selected" 
    bpy.ops.object.duplicate_move()
       
    # the duplicate is active, apply all transforms to get global coordinates
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    # convert to mesh
    bpy.ops.object.convert(target='MESH', keep_original=False)
    

    _data = context.active_object.data
    
    edge_length = 0
    for edge in _data.edges:
        vert0 = _data.vertices[edge.vertices[0]].co
        vert1 = _data.vertices[edge.vertices[1]].co
        edge_length += (vert0-vert1).length
    
    # deal with trailing float smear
    to_ret = edge_length
    edge_length = '{:.6f}'.format(edge_length)
    print(edge_length)
    
    # stick into clipboard
    context.window_manager.clipboard = edge_length
    
    bpy.ops.object.delete()
    context.scene.objects.active = context.scene.objects[obj_name_original]
    context.object.select = True
    
    return to_ret
        
def toggle():
    bpy.ops.object.editmode_toggle() 
    
def deselect_all(): 
    for obj in bpy.data.objects:
        obj.select = False
def activate(obj):
    obj.select = True
    bpy.context.scene.objects.active = obj
            
def get_braid_obj(braid_ind):
    seeking = 'Braid.%d' % braid_ind
    for obj in bpy.data.objects: 
        if seeking in obj.name:
            obj.select = True
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
            return obj 

def check_name(name): 
    print(name)
    for obj in bpy.data.objects:
        if name == obj.name:
            return True 
        
def get_curve_midpoint(braid, curve, length):
    print(curve.data.splines.active.points)   
    print(braid.location[1]) 
    curve.rotation_euler[0] = 0.0
    curve.rotation_euler[2] = 0.0
    #braid.location[1] = curve.data.splines.active.points[3].co.y
    braid.location[1] = curve.location[1] - length/2
    braid.location[0] = curve.location[0]
    braid.location[2] = curve.location[2]
    print("post:") 
    print(braid.location[1])

def wrap_to_obj(curve, target_obj):
    shrinkwrap = curve.modifiers.new("ShrinkWrap", 'SHRINKWRAP')
    shrinkwrap.target = bpy.data.objects[target_obj]

    shrinkwrap.modifier_apply()

        
def braid_on_curve(braid_obj, curve, length):
    
    #bpy.ops.object.convert(target='MESH')

    curve_mod = braid_obj.modifiers.new("Curve", 'CURVE')

    #if (curve == ""):
        
    #    #name = bpy.data.curves[0].name
    #    if 'Braid' in bpy.data.objects[0].name:
    #        name = bpy.data.objects[3].name
    
    if check_name(curve.name):
        curve_mod.object = curve #bpy.data.objects[name] 
        curve_mod.deform_axis = "NEG_Y"
        get_curve_midpoint(braid_obj, curve, length)
        #braid_obj.location[1] -= 14
        
    else: 
        print("Please enter the name of a curve in this scene") 
        

def edgeloop_convert(name, num_braids, to_braid): 
    #go into editmode
    toggle() 
    edges= (len(to_braid.data.edges))
    for i in range (edges): 
        to_braid.data.edges[i].select = True
        print(i)
        print (to_braid.data.edges[i].select) 
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode": 1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    
    print("pop") 
    
def clear():
    #for obj in bpy.data.objects:
    #    if obj.type not in ('CAMERA', 'LAMP'):
    #        obj.select = True
    #    else:
    #        obj.select = False
    for obj in bpy.data.objects:
        if 'circle' in obj.name:
            obj.select = True 
        else: 
            obj.select = False 
    
    bpy.ops.object.delete()
    

def find_obj_name(name):
    deselect_all() 
    if name == "":
        print("Please enter the name of the object you would like be braided.") 
        return "No" 
    for obj in bpy.data.objects:
        if name in obj.name:
            obj.select = True
            bpy.context.scene.objects.active = obj 
            print("Is this the correct object?:") 
            print (obj.name)
            return obj
        
    return ("No object of that name found!") 
            
def spline(objname, curvename, points, lines, round, bevel =None, join=True, type = 'NURBS'):
    curve = bpy.data.curves.new(name=curvename, type='CURVE')  
    curve.dimensions = '3D'
  
    obj = bpy.data.objects.new(objname, curve)  
    obj.location = (0,0,0) #object origin  
    bpy.context.scene.objects.link(obj)
    
    if round:
        for i, line in enumerate(lines):
            
            polyline = curve.splines.new(type)
            polyline.points.add(len(line)-1)  
            for num in range(len(line)):
                polyline.points[num].co = (line[num])+(1,)  
  
            polyline.order_u = len(polyline.points)-1
            if join:
                polyline.use_cyclic_u = True

        curve.bevel_object = bpy.data.objects[bevel]
        return obj
    else: 
        polyline = curve.splines.new(type)
        polyline.points.add(len(points)-1)  
        for num in range(len(points)):
            polyline.points[num].co = (points[num])+(1,)  
  
        polyline.order_u = len(polyline.points)-1
        if join:
            polyline.use_cyclic_u = True

        if bevel:
            curve.bevel_object = bpy.data.objects[bevel]
        return obj
        

def mul(x, items):
    return tuple(x*b for b in items)


def braid_strand(length, strands, strandnum, x_width, y_width, height, taper, x0=0, y0=None, ds = None, resolution=1):

    if y0 is None:
        y0 = -length * strands / 2
    if ds is None:
        ds = strands * 2
    steps = (strands - 1)*2

    a = pi/steps
    b = pi/2
    
    dy = 2 * pi / strands / a
    y0 += strandnum * dy * y_width
    i0 = 0 if not taper else - strandnum * (strands + ds) / 4
    for y in range(length * steps * resolution):
        y /= resolution
        y += i0
        x = cos(a*y)*x_width
        z = sin(b*y)*height
        yield mul(1, (x + x0, y * y_width + y0, z))

def make_braid(name, strands, length, x_width, y_width, height, taper, bevel='circle'):
    lines = []
    for i in range(strands):
        strand = tuple(braid_strand(length, strands, i, x_width, y_width, height, taper))
        #if circle:
            #strand = tuple(circlify(strand))
        lines.append(strand)
    return spline(name, name + '_curve', lines, lines, True, bevel, False)

def generate_single_braid(braid_name, num_strands, length, x_width, height, y_width, strand_width, strand_height, taper):
    #clear()
    w = strand_width
    h = strand_height
    num_braids = count_braids() 
    name = 'circle.%d' % num_braids   
    pts = [(-strand_width/2, 0, 0), (0, -strand_height/2, 0), (strand_width/2, 0, 0), (0, strand_height/2, 0)]
    spline(name, name, pts, pts, False)
    make_braid(braid_name, num_strands, length, x_width, y_width, height, taper=True, bevel=name)
    
def get_curvemidpoint(curve):
    print(curve.data.splines.points)
    
    


class Braid(bpy.types.Operator):
    bl_idname = 'mesh.make_braid'
    bl_label = 'New Braid'
    bl_description = 'Create a new braid'
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    
    
    num_strands = IntProperty(name = 'Strands' , min = 2, max = 3, default = 3)
    length = IntProperty(name = 'Length', min = 1, max = 100, default = 30) 
    x_width = FloatProperty(name = 'X Width', min = 0.1, max = 1.0, default = 0.3) 
    height = FloatProperty(name = 'Height', min = 0.1, max = 1.0, default = 0.1) 
    y_width = FloatProperty(name = 'Y Width', min = 0.1, max = 1.0, default = 0.2)
    #braid_name = StringProperty(name = 'Braid Name', default = 'Braid')
    
    
    strand_width = FloatProperty(name = 'Strand Width', min =0.1, max = 1.0, default = 0.6)
    strand_height = FloatProperty(name = 'Strand Height', min =0.1, max= 1.0, default = 0.6)
    target_obj = StringProperty(name = 'Object to Braid', default = 'Group49317') 
    scale = FloatProperty(name = 'Scale', min =0.1, max = 5.0, default = 1)
    wrap = BoolProperty(name = 'Wrap Curve', default = True) 
    
    braiding_type = bpy.props.EnumProperty(
                                name = "Braid Placement",
                                default = "0",
                                description = "Braid Placement" ,
                                items = [
                                    ("0", "Single Curve", "Create a single curve for the braid shape", 0),
                                    ("1", "Single Edge Loop", "Place a Braid along the edge loop of an object", 1),
                                    ("2", "All Edge Loops", "Place Braids on each edge loop of the object", 2),
                                    ("3", "Every Other Edge Loop", "Place Braids on every other edge loop of the object", 3),
                                    ("4", "Circle Braid", "Create a Circle Braid", 4),
                                    ]
                            )

    
    def execute(self, context):
       
        self.length = get_length(context)
        save_len = self.length 
        self.length += self.length / 1.2
        if self.scale < 1: 
            self.length = (1/self.scale) * self.length 
        
        if(self.length == "No Object Selected"):
            return {'FINISHED'}
        to_braid = bpy.context.active_object
        curve = to_braid
        print(len)
        
        braid_ind = count_braids()  
        braid_name = 'Braid.%d' % braid_ind
        curve_length = generate_single_braid(braid_name, self.num_strands, self.length, self.x_width, self.height, self.y_width, self.strand_width, self.strand_height, taper = True) 
       
        obj = get_braid_obj(braid_ind)
        #get_length(self.object_to_braid_name)
        obj.scale *= self.scale
        
            
        if self.braiding_type == "0": 
            print(curve)
            #wrap_to_obj(curve, self.target_obj) 
            braid_on_curve(obj, curve, save_len)
            
            #get_length(context)
        elif self.braiding_type == "1":
            
            print ("single EDGELOOP !") 
        elif self.braiding_type == "2":
            obj.hide= True 
            print("we're looking for the obj name, which is the line below:")
            print(obj.name) 
            #print(self.object_to_braid_name) 
            to_braid = find_obj_name(self.object_to_braid_name)
            #num_braids = IntProperty(name = 'Number of Braids on Object', default = len(to_braid.data.edges)) 
            num_braids = 2
            if (to_braid == "No"):
                self.braiding_type = "0" 
            else:
                edgeloop_convert(self.object_to_braid_name, num_braids, to_braid)
            
            print ("ALL EDGELOOP !") 
        elif self.braiding_type == "3":
            print ("other EDGELOop!") 
        elif self.braiding_type == "4":
            print ("circlify") 
    
        
        
        return {'FINISHED'}



class BraidButton (bpy.types.Panel): 
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Create"
    bl_label = "Braid Test"


    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("mesh.make_braid", text = "Create Braid Along Curve")


def register():
    bpy.utils.register_class(Braid)
    bpy.utils.register_class(BraidButton) 


register()