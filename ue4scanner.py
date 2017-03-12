bl_info = {
    "name": "Unreal Engine 4 Scanner",
    "description": "Scans a blend file for use in Unreal Engine.",
    "author": "Mike Rovers",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "View3D",
    "warning": "This is an unstable version",
    "wiki_url": "",
    "category": "Object" 
}

import bpy
from bpy.props import *

def GetContextObjects(useContext):
    if(useContext):
        return bpy.context.selected_objects
    else:
        return null
    
class Messages(object):
    messages = []

    @classmethod
    def get_messages(self):
        return self.messages
    
    @classmethod
    def clear_messages(self):
        self.messages = []
        
    @classmethod
    def add_message(self, message):
        self.messages.append(message)
    
    @classmethod
    def show_messages(self):
        bpy.ops.error.message('INVOKE_DEFAULT', type="Error")
        self.messages[:] = []
    
class MessageOperator(bpy.types.Operator):
    bl_idname = "error.message"
    bl_label = "Message"
    type = StringProperty()
    messages = Messages.get_messages()
 
    def execute(self, context):
        self.report({'INFO'}, self.bl_label)
        print(self.bl_lable)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=600)
 
    def draw(self, context):
        self.layout.label("A message has arrived")
        row = self.layout.split(0.25)
        for message in self.messages:       
            self.layout.label(message)

        row = self.layout.split(0.80)
        row.label("") 
        row.operator("error.ok")
    
class OkOperator(bpy.types.Operator):
    bl_idname = "error.ok"
    bl_label = "OK"
    def execute(self, context):
        return {'FINISHED'}

class ScanTransformApplied(bpy.types.Operator):
    """Check if the all transforms are applied."""
    bl_idname = "object.scantransform"
    bl_label = "Scan Transformations"
    
    messages = []
    
    def ScanScale(self, object):
        if not (object.scale.x == 1 and object.scale.y == 1):
            return False
        else:
            return True
        
    def ScanRotation(self, object):
        if not (object.rotation_euler.x == 0 and object.rotation_euler.y == 0 and object.rotation_euler.z == 0):
            return False
        else:
            return True
    
    def execute(self, context):
    
        objects = GetContextObjects(True)
        for obj in objects:
            if not self.ScanScale(obj):
                Messages.add_message(("%s\'s scale is not set to 1." % obj.name));
            if not self.ScanRotation(obj):
                Messages.add_message(("%s\'s rotation is not set to 0." % obj.name));
            
        Messages.show_messages()        
    
        return {'FINISHED'}
        
class AppliedPanel(bpy.types.Panel):
    bl_label = "Unreal Engine 4 Scanner"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "UE4Scan"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.scantransform")
        layout.prop

def register():
    bpy.utils.register_class(AppliedPanel)
    bpy.utils.register_class(ScanTransformApplied)
    bpy.utils.register_class(MessageOperator)

def unregister():
    bpy.utils.unregister_class(AppliedPanel)
    bpy.utils.unregister_class(ScanTransformApplied)
    bpy.utils.unregister_class(MessageOperator)

if __name__ == "__main__":
    register()