# **************************************************************************************************************
# content       = checks if the asset has keyframes
#
# dependencies  = Maya
#
# author  = Stephane Barbin
# **************************************************************************************************************

import maya.cmds as cmds

# **************************************************************************************************************


def list_animated_attributes(obj):
    """
    Returns information about animation keys on mesh objects in scene

    Args:
        obj (str): mesh object's name

    Returns:
        list: names of the mesh object's animated attributes
    """
    animatable_attrs = cmds.listAnimatable(obj)
    animated_attributes = []

    # Checking each animatable attribute to see if it has keyframes
    for attr in animatable_attrs:
        keyframes = cmds.keyframe(attr, query=True)
        if keyframes:
            attribute_name = attr.split(".")[-1]
            animated_attributes.append(attribute_name)

    return animated_attributes


def delete_keyframes(obj, attribute):
    full_attribute = obj + '.' + attribute
    cmds.cutKey(full_attribute, clear=True)


def animated_objects(button_clicked):
    """
    Main function called from the UI to check if objects have animated attributes

    Args:
        button_clicked (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'

    Returns:
        str: Status of the qc check i.e.: passed, warning or failed
        dict: Report of names and animated attributes info of each object when check fails
        int: A flag sent back to the main: 0 for passed, 1 for failed
    """
    status_flag = 'passed'
    default_cameras = ['persp', 'top', 'front', 'side']
    button_switch = 0

    top_level_objects = cmds.ls(assemblies=True)

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
        animated_objects_report = {}
        report_list = []
        
        # Check if object has keyframes
        for asset_mesh in polygon_meshes:
            transform = cmds.listRelatives(asset_mesh, parent=True)[0]

            # Calling function to retrieve attributes
            animated_attribs = list_animated_attributes(transform)

            if animated_attribs:
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
        status_flag = 'passed'
        animated_objects_report = {}
        report_list = []

        # Calling delete_keyframe function to delete keyframes for object's attributes
        for asset_mesh in polygon_meshes:
            transform = cmds.listRelatives(asset_mesh, parent=True)[0]
            animated_attribs = list_animated_attributes(transform)
            for attr in animated_attribs:
                delete_keyframes(transform, attr)
    
    return (status_flag,
            animated_objects_report,
            button_switch
            )
