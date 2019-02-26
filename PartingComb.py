import bpy  
from mathutils import Vector 
from math import sin, cos, pi 
from bpy.props import  (FloatProperty,
                        FloatVectorProperty,
                        IntProperty,
                        BoolProperty,
                        StringProperty)

def get_parting_points(context, grease):
    if grease:
        print("accessing grease pencil data...")

    else:
        curve = bpy.data.objects["NurbsPath"]
        spline = curve.data.splines[0]
        curve_points = spline.points
        return curve_points

    return False

def  part_hair_along_points (curve_points, context, strength, radius):
    print("getting hairs...")
     #print(curve_points[p].co.x)
     ##print(curve_points[p].co.y)
     #print(curve_points[p].co.z)
    radius = radius / 10 
    print(radius)
    shortest_distance =100 
    #strength = strength / 2
    print('strength: {i}'.format(i=strength))

    prev_shortest = shortest_distance
    for p in range (len(curve_points)):
       hairs = context.object.particle_systems[0].particles
       for i, h in enumerate(hairs): 
            print('hair number {i}:'.format(i=i))
            for i, hv in enumerate(h.hair_keys):
                print('  vertex {i} coordinates: {co}'.format(i=i, co=hv.co))
                x_diff = abs(hv.co.x - curve_points[p].co.x)
                y_diff = abs(hv.co.y - curve_points[p].co.y) 
                #z_diff = abs(hv.co.z - curve_points[p].co.z)

                hair_x = hv.co.x
                hair_y = hv.co.y 
                hair_z = hv.co.z
               
                #print("X_DIFF: %f\n", x_diff)
                #print("Y_DIFF: %f\n", y_diff)

                if x_diff <= radius:
                    #print(y_diff)
                    #print("move hair's y coord!")
                    
                    print("X_POINT: %f" % hair_x)
                    if hair_x > curve_points[p].co.x:
                        print("adding... ")
                        hair_x = hair_x + strength 
                    else :
                        print("subtracting...")
                        hair_x = hair_x - strength 
                    #hv.co.y = curr_hair_point


                if y_diff <= radius:
                    #print(x_diff)
                    #print("move hair's x coord!"
                    print("Y: %f" % hair_y)
                    if hair_y > curve_points[p].co.y:
                        print("adding... ")
                        hair_y = hair_y + strength 
                    else :
                        print("subtracting...")
                        hair_y = hair_y - strength 
                    
                #if z_diff <= radius:
                    #print(z_diff)
                    #print("move hair's z coord!")
                #    print("Z: %f\n" % hair_z)
                #    if hair_z > curve_points[p].co.z:
                #        hair_z += strength
                #    else :
                #        hair_z -= strength
                    
                hv.co = (hair_x, hair_y, hair_z) 
                print('The result:  {hv} \n'.format(hv=hv.co)) 
               
                    

class AfroRender_PartingComb (bpy.types.Operator):
    bl_idname = "object.parting_comb"
    bl_label = "Use Parting Comb for Hair Groom"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    grease = bpy.props.BoolProperty(name = "Grease Pencil", description = "Use Grease Pencil as a Parting Curve", default = False)
    strength = bpy.props.IntProperty(name = "Strength", description = "Strength of Parting Comb", min = 1, max = 10, default = 5)
    radius = bpy.props.IntProperty(name="Radius", description = "Distance Parting Comb will effect", min = 1, max = 100, default = 10)

    def execute (self, context):
        print("Parting Comb Operator has been activiated")

        curve_points = get_parting_points(context, self.grease)
        print(curve_points)
        part_hair_along_points(curve_points, context, self.strength, self.radius)


        return {'FINISHED'}

class AfroRender_PartingCombPanel(bpy.types.Panel):
    
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "particlemode"
    bl_category = "Tools"
    bl_label = "Parting Comb"

    def draw(self, context):
        layout = self.layout
        NaturalHair = layout.row()
        NaturalHair.label(text = "Parting Comb Test 1")
        NaturalHair.operator("object.parting_comb", text = "Parting Comb")
        print("panel function for parting comb")


def register():
    bpy.utils.register_class(AfroRender_PartingComb)
    bpy.utils.register_class(AfroRender_PartingCombPanel)

register()
