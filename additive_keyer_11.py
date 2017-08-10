# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
	"name": "Additive keyer",
	"author": "Artell",
	"version": (1, 0),
	"blender": (2, 7, 5),
	"location": "3D View > Tool Shelf > Animation",
	"description": "Allows armatures interactive keying on an additive NLA strip (additive animation layer)",	
	"category": "Animation"}

import bpy, math
from mathutils import Matrix, Vector


print('\n Starting Additive keyer... \n')

		
class key_rot(bpy.types.Operator):
	""" Key the current rotation on the additive action, while preserving the base action value. 0 to reset. """
	
	bl_idname = "id.key_additive_rot"
	bl_label = "key_additive_rot"
	bl_options = {'UNDO'}	

	value = bpy.props.IntProperty()
	
	@classmethod
	def poll(cls, context):
		if context.object.mode == 'POSE':
			return True

	def execute(self, context):
		use_global_undo = context.user_preferences.edit.use_global_undo
		context.user_preferences.edit.use_global_undo = False		
		
		#save current mode
		try:			

			_key_additive_rot(self.value)
			
		finally:
			context.user_preferences.edit.use_global_undo = use_global_undo
		return {'FINISHED'}
		
class key_loc(bpy.types.Operator):
	""" Key the current location on the additive action, while preserving the base action value. 0 to reset."""
	
	bl_idname = "id.key_additive_loc"
	bl_label = "key_additive_loc"
	bl_options = {'UNDO'}	

	value = bpy.props.IntProperty()
	
	@classmethod
	def poll(cls, context):
		if context.object.mode == 'POSE':
			return True

	def execute(self, context):
		use_global_undo = context.user_preferences.edit.use_global_undo
		context.user_preferences.edit.use_global_undo = False		
		
		#save current mode
		try:
			_key_additive_loc(self.value)
			
		finally:
			context.user_preferences.edit.use_global_undo = use_global_undo
		return {'FINISHED'}

class key_scale(bpy.types.Operator):
	""" Key the current scale on the additive action, while preserving the base action value. 0 to reset."""
	
	bl_idname = "id.key_additive_scale"
	bl_label = "key_additive_scale"
	bl_options = {'UNDO'}	

	value = bpy.props.IntProperty()
	
	@classmethod
	def poll(cls, context):
		if context.object.mode == 'POSE':
			return True

	def execute(self, context):
		use_global_undo = context.user_preferences.edit.use_global_undo
		context.user_preferences.edit.use_global_undo = False		
		
		#save current mode
		try:
			_key_additive_scale(self.value)
			
		finally:
			context.user_preferences.edit.use_global_undo = use_global_undo
		return {'FINISHED'}
	
#FUNCTIONS ############################################################


		
def set_active_object(object_name):
	 bpy.context.scene.objects.active = bpy.data.objects[object_name]
	 bpy.data.objects[object_name].select = True	

def _key_additive_rot(value):
	scene = bpy.context.scene
	obj = bpy.context.active_object	
	bones = bpy.context.selected_pose_bones
	base_layer = bpy.data.actions[obj.key_base_action]	
	current_frame = bpy.context.scene.frame_current
	
	#disable auto key if enabled
	scene.tool_settings.use_keyframe_insert_auto = False	
	
	for bone in bones:	
		if bone.rotation_mode != 'QUATERNION':
			max_range = 3
			dpath = 'rotation_euler'
		else:
			max_range = 4
			dpath = 'rotation_quaternion'
	
		for i in range(0, max_range):		
			#reset
			if value == 0:				
				add_fcurve = obj.animation_data.action.fcurves.find('pose.bones["' + bone.name + '"].' + dpath, index = i)
				if add_fcurve != None:
					add_value = add_fcurve.evaluate(current_frame)	
					if bone.rotation_mode != 'QUATERNION':
						bone.rotation_euler[i] -= add_value
					else:
						bone.rotation_quaternion[i] -= add_value
				else:
					print("No additive fcurve found")
				
			#current key			
			base_fcurve = base_layer.fcurves.find('pose.bones["' + bone.name + '"].' + dpath, index = i)
			if base_fcurve != None:
				base_value = base_fcurve.evaluate(current_frame)
				if bone.rotation_mode != 'QUATERNION':
					bone.rotation_euler[i] -= base_value
				else:
					bone.rotation_quaternion[i] -= base_value
			else:
				print("No base fcurve found")
		
		if base_fcurve != None:
			if bone.rotation_mode != 'QUATERNION':
				bone.keyframe_insert(data_path = "rotation_euler")
			else:
				bone.keyframe_insert(data_path = "rotation_quaternion")
	
	#update hack
	bpy.context.scene.frame_set(current_frame)
	
def _key_additive_loc(value):
	scene = bpy.context.scene
	obj = bpy.context.active_object
	bones = bpy.context.selected_pose_bones
	base_layer = bpy.data.actions[obj.key_base_action]	
	current_frame = bpy.context.scene.frame_current
	
	#disable auto key if enabled
	scene.tool_settings.use_keyframe_insert_auto = False
	
	
	for bone in bones:		
		for i in range(0,3):		
			#reset
			if value == 0:				
				add_fcurve = obj.animation_data.action.fcurves.find('pose.bones["' + bone.name + '"].location', index = i)
				add_value = add_fcurve.evaluate(current_frame)				
				bone.location[i] -= add_value
				
			#current key			
			base_fcurve = base_layer.fcurves.find('pose.bones["' + bone.name + '"].location', index = i)
			base_value = base_fcurve.evaluate(current_frame)			
			bone.location[i] -= base_value
				
		bone.keyframe_insert(data_path = "location")
	
	#update hack
	bpy.context.scene.frame_set(current_frame)
	
def _key_additive_scale(value):
	scene = bpy.context.scene
	obj = bpy.context.active_object
	bones = bpy.context.selected_pose_bones
	base_layer = bpy.data.actions[obj.key_base_action]	
	current_frame = bpy.context.scene.frame_current
	
	#disable auto key if enabled
	scene.tool_settings.use_keyframe_insert_auto = False
	
	
	for bone in bones:		
		for i in range(0,3):		
			#reset
			if value == 0:				
				add_fcurve = obj.animation_data.action.fcurves.find('pose.bones["' + bone.name + '"].scale', index = i)
				add_value = add_fcurve.evaluate(current_frame)				
				bone.scale[i] -= add_value
				
			#current key			
			base_fcurve = base_layer.fcurves.find('pose.bones["' + bone.name + '"].scale', index = i)
			base_value = base_fcurve.evaluate(current_frame)			
			bone.scale[i] -= base_value
				
		bone.keyframe_insert(data_path = "scale")
	
	#update hack
	bpy.context.scene.frame_set(current_frame)


	
	
def set_active_bone(bone):
	bpy.context.object.data.bones.active = bpy.context.object.pose.bones[bone].bone
	


#UI PANEL ##########################################################
class additive_keyer(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Animation'
	bl_label = "Additive keyer"
	bl_idname = "id_additive_keyer"	
   
	
	@classmethod
	# button visibility conditions
	def poll(cls, context):
		if bpy.context.active_object != None:
			return True
	
	

	def draw(self, context):
		layout = self.layout.column(align=True)		
		object = context.active_object		  
		scene = context.scene	
		
		#layout.label("Additive keyer:")
		layout.label("Base Action")
		layout.prop_search(object, "key_base_action", bpy.data, "actions", "")
		#layout.label("Additive Action")
		#layout.prop_search(scene, "key_additive_action", bpy.data, "actions", "")
		layout.separator()
		row = layout.row(align=True)
		btn = row.operator("id.key_additive_loc", "Loc", icon="KEY_HLT")
		btn.value = 1
		btn = row.operator("id.key_additive_loc", "0")
		btn.value = 0
		row = layout.row(align=True)
		btn = row.operator("id.key_additive_rot", "Rot", icon="KEY_HLT")
		btn.value = 1
		btn = row.operator("id.key_additive_rot", "0")
		btn.value = 0
		row = layout.row(align=True)
		btn = row.operator("id.key_additive_scale", "Scale", icon="KEY_HLT")
		btn.value = 1
		btn = row.operator("id.key_additive_scale", "0")
		btn.value = 0
		
		
	  
#REGISTER

def register():
	bpy.utils.register_module(__name__) 
	
	bpy.types.Object.key_base_action = bpy.props.StringProperty(name="Base Action", description="Base action", default ="")
	#bpy.types.Scene.key_additive_action = bpy.props.StringProperty(name="Additive Action", description="Additive action", default ="")
	
	
def unregister():
	bpy.utils.unregister_module(__name__)	

	del bpy.types.Object.key_base_action
	#del bpy.types.Scene.key_additive_action
	
if __name__ == "__main__":
	register()
