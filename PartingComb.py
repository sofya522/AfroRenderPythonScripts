import bpy

class AfroRender_PartingComb (bpy.types.Operator):
    bl_idname = "object.parting_comb"
    bl_label = "Use Parting Comb for Hair Groom"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def execute (self, context):
        print("Parting Comb Operator has been activiated")
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
