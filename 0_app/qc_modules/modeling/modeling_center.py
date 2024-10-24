# Modeling Center Check **********************************************************************
# 
# This is the quality check "center". It checks if the asset is in the world center.
#
# date    = 2024-08-30
# author  = Stephane Barbin
#*********************************************************************************************



# Importing modules
import maya.cmds as cmds

# Function for the modeling qc center check
def meshes_center(button_clicked):
    # Initializing
    status_flag = 'passed'
    default_cameras = ['persp', 'top', 'front', 'side']
    button_switch = 0

    # Getting all top-level transforms in the scene
    top_level_objects = cmds.ls(assemblies=True)

    # List of "mesh" type objects for the qc check
    polygon_meshes = []

    for top_object in top_level_objects:
        if top_object not in default_cameras:
            shape_objects = cmds.listRelatives(top_object, shapes=True) or []
            for shape in shape_objects:
                if cmds.nodeType(shape) == 'mesh':
                    polygon_meshes.append(shape)
                    break

    # Running the check
    if button_clicked == 'run_button':
        # Dictionary and list for the report
        center_report = {}
        report_list = []

        # Check if centered
        for asset_mesh in polygon_meshes:
            transform = cmds.listRelatives(asset_mesh, parent=True)[0]

            # Assigning position x, y z
            asset_posx = cmds.getAttr(transform + '.translateX')
            asset_posy = cmds.getAttr(transform + '.translateY')
            asset_posz = cmds.getAttr(transform + '.translateZ')

            asset_posx_rounded = round((asset_posx), 2)
            asset_posy_rounded = round((asset_posy), 2)
            asset_posz_rounded = round((asset_posz), 2)

            # If not in center of word
            if asset_posx != 0 or asset_posy != 0 or asset_posz != 0:
                # Check has failed
                status_flag = 'failed'

                # Filling the list report
                if transform not in center_report:
                    center_report[transform] = []
                report_list.append("<b style='color:rgb(255,0,0);'>Center failed:</b> " + 'Object ' + str(transform) + ' position ' + 'is: ' + str(asset_posx_rounded) + ' ,' + str(asset_posy_rounded) + ' ,' + str(asset_posz_rounded))
                center_report[transform].append(report_list)
            else:
                status_flag = 'passed'
        
    # Running the fix
    elif button_clicked == 'fix_button':
        # Initializing for the fix pass
        status_flag = 'passed'
        center_report = {}
        report_list = []

        # Putting in center of world
        for asset_mesh in polygon_meshes:
            transform = cmds.listRelatives(asset_mesh, parent=True)[0]
            cmds.setAttr(transform + '.translateX', 0)
            cmds.setAttr(transform + '.translateY', 0)
            cmds.setAttr(transform + '.translateZ', 0)
    
    return status_flag, center_report, button_switch
