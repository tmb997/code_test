import bpy
import math
import numpy as np
from datetime import date 

def change_camera(cnum):
    context = bpy.context
    scene = context.scene
    currentCameraObj = bpy.data.objects["Camera"+"."+"00"+str(cnum)]
    scene.camera = currentCameraObj
    
def take_pict(num_pic):
    for i in range(1,num_pic+1):
        change_camera(i)
        bpy.context.scene.render.filepath = 'C:/Users/tomib/Desktop/Thesis/3d Model/Renders/Img_Cam-00'+str(i)+str(date.today())+'.jpg'
        bpy.ops.render.render(write_still = True) 


def set_rot2(rot_ang):
    bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.user_transforms_clear()
    bpy.ops.pose.select_all(action='DESELECT')
    
    for i in range(6,-1,-1):
        bone_i="Bone"+"."+"00"+str(i+1)
    
        bpy.data.objects["Armature"].data.bones[bone_i].select = True
        
        or_ax='Y'
        co_ax=(True, False, False)
        
        if i in [6,4,1]:
            or_ax='Z'
            co_ax=(False, False, True)
                
        bpy.ops.transform.rotate(value=rot_ang[i], orient_axis=or_ax,\
        orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),\
        orient_matrix_type='GLOBAL', constraint_axis=co_ax,\
        mirror=True, use_proportional_edit=False,proportional_edit_falloff='SMOOTH',\
        proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        

        bpy.data.objects["Armature"].data.bones[bone_i].select = False
        
ang_deg=[0,0,-15,-75,0,0,158s]         
#ang_deg=[0,0,0,0,0,0,0]     
rot_ang=np.array(ang_deg)/180*math.pi
        
set_rot2(rot_ang)
#take_pict(2)
