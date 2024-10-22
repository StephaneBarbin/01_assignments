# Modeling Animated Objects Check ************************************************************
# 
# This is the quality check "animated objects". It checks if the asset has keyframes.
#
# date    = 2024-08-30
# author  = Stephane Barbin
#*********************************************************************************************



# Importing modules
import maya.cmds as cmds

# Function to return animated attributes
def list_animated_attributes(obj):
    # Getting all animatable attributes of the object
    animatable_attrs = cmds.listAnimatable(obj)
    
    animated_attributes = []

    # Checking each animatable attribute to see if it has keyframes
    for attr in animatable_attrs:
        keyframes = cmds.keyframe(attr, query=True)
        if keyframes:
            # Extract the attribute name from the full path
            attribute_name = attr.split(".")[-1]
            animated_attributes.append(attribute_name)

    return animated_attributes


# Function to delete keyframes
def delete_keyframes(obj, attribute):
    full_attribute = obj + '.' + attribute
    cmds.cutKey(full_attribute, clear=True)


# Function for the modeling qc animated objects check
def animated_objects(button_clicked):
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
        animated_objects_report = {}
        report_list = []
        
        # Check if object has keyframes
        for asset_mesh in polygon_meshes:
            transform = cmds.listRelatives(asset_mesh, parent=True)[0]

            # Calling function to retrieve attributes
            animated_attribs = list_animated_attributes(transform)

            # If there are animated attributes
            if animated_attribs:
                # Check has failed
                status_flag = 'failed'

                # Creating a list to add to the end of the list report
                string_to_append = ''
                for attr in animated_attribs:
                    string_to_append = ', '.join(animated_attribs)
                
                # Filling the list report
                animated_objects_report[transform] = []
                report_list.append("<b style='color:rgb(255,0,0);'>Animated Objects failed:</b> " + 'Object ' + str(transform) + ' has keyframes on the following attributes: ' + string_to_append)
                
                animated_objects_report[transform].append(report_list)
            else:
                status_flag = 'passed'
    
    # Running the fix    
    elif button_clicked == 'fix_button':
        # Initializing for the fix pass
        status_flag = 'passed'
        animated_objects_report = {}
        report_list = []

        # Calling delete_keyframe function to delete keyframes for object's attributes
        for asset_mesh in polygon_meshes:
            transform = cmds.listRelatives(asset_mesh, parent=True)[0]
            animated_attribs = list_animated_attributes(transform)
            for attr in animated_attribs:
                delete_keyframes(transform, attr)
    
    return status_flag, animated_objects_report, button_switch
