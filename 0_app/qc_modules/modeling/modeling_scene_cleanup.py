# Scene Cleanup Check ************************************************************************
# 
# This is the quality check "scene cleanup". It checks for modeling department's illegal objects.
#
# date    = 2024-08-30
# author  = Stephane Barbin
#*********************************************************************************************



# Importing modules
import maya.cmds as cmds

# Function for the modeling qc illegal objects check
def illegal_cleanup(button_clicked):
    status_flag = 'passed'
    default_cameras = ['persp', 'top', 'front', 'side']
    button_switch = 0

    # Getting all top-level transforms in the scene
    top_level_objects = cmds.ls(assemblies=True)

    # List of objects other than "mesh" type for the qc check
    illegal_objects = []

    for top_object in top_level_objects:
        if top_object not in default_cameras:
            shape_objects = cmds.listRelatives(top_object, shapes=True) or []
            for shape in shape_objects:
                if cmds.nodeType(shape) != 'mesh':
                    illegal_objects.append(shape)
                    break

    # Running the check
    if button_clicked == 'run_button':
        # Dictionary and list for the report
        cleanup_report = {}
        report_list = []
        comma_counter = 0

        # Check if illegal object list not empty
        if illegal_objects:
            # Check has failed
            status_flag = 'failed'

            # Filling the list report
            cleanup_report = {'illegal_objects' : []}
            report_list = ["<b style='color:rgb(255,0,0);'>Scene Cleanup failed:</b> " + 'Scene has illegal objects: ']
            for asset_mesh in illegal_objects:
                comma_counter += 1
                transform = cmds.listRelatives(asset_mesh, parent=True)[0]
                # Checking if we put a comma after the object...
                if comma_counter != len(illegal_objects):
                    report_list[0] += (str(transform) + ', ')
                # ...or no comma, if it's the last object of the list
                else:
                    report_list[0] += (str(transform))
            cleanup_report['illegal_objects'].append(report_list)
                    
        else:
            status_flag = 'passed'

    # Running the fix
    elif button_clicked == 'fix_button':
        # Initializing for the fix pass
        status_flag = 'passed'
        cleanup_report = {}
        report_list = []

        # Deleting illegal objects
        for asset_mesh in illegal_objects:
            transform_object = cmds.listRelatives(asset_mesh, parent=True)[0]
            cmds.delete(transform_object)
            
    return status_flag, cleanup_report, button_switch
