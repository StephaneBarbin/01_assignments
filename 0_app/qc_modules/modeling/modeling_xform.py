# **************************************************************************************************************
# content       = checks if the asset has rotation or scale values
#
# how to        =
# dependencies  = Maya
# to dos        =
#
# author  = Stephane Barbin
# **************************************************************************************************************



import maya.cmds as cmds



# **************************************************************************************************************



def meshes_xform(button_clicked):
    """
    Main function called from the UI to check for objects with rotation or scale values

    Args:
        button_clicked (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'

    Returns:
        str: Status of the qc check i.e.: passed, warning or failed
        dict: Report of names and rotation or scale coordinates info of each object when check fails
        int: A flag sent back to the main: 0 for passed, 1 for failed
    """
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
        xform_report = {}
        report_list = []

        # Check if rotation or scale are not zeroed out
        for asset_mesh in polygon_meshes:
            transform = cmds.listRelatives(asset_mesh, parent=True)[0]

            # Assigning rotation x, y z
            asset_rotx = cmds.getAttr(transform + '.rotateX')
            asset_roty = cmds.getAttr(transform + '.rotateY')
            asset_rotz = cmds.getAttr(transform + '.rotateZ')

            asset_rotx_rounded = round((asset_rotx), 2)
            asset_roty_rounded = round((asset_roty), 2)
            asset_rotz_rounded = round((asset_rotz), 2)

            # Assigning scale x, y z
            asset_scalex = cmds.getAttr(transform + '.scaleX')
            asset_scaley = cmds.getAttr(transform + '.scaleY')
            asset_scalez = cmds.getAttr(transform + '.scaleZ')

            asset_scalex_rounded = round((asset_scalex), 2)
            asset_scaley_rounded = round((asset_scaley), 2)
            asset_scalez_rounded = round((asset_scalez), 2)

            # If there's values
            if (asset_rotx != 0 or asset_roty != 0 or asset_rotz != 0) or (asset_scalex != 1 or asset_scaley != 1 or asset_scalez != 1):
                # Check has failed
                status_flag = 'failed'

                # Filling the list report
                if asset_rotx != 0 or asset_roty != 0 or asset_rotz != 0:
                    # Filling the report for rotation
                    if transform not in xform_report:
                        xform_report[transform] = []
                    report_list.append("<b style='color:rgb(255,0,0);'>Freeze Transform failed:</b> " + 'Object ' + str(transform) + ' rotation ' + 'is: ' + str(asset_rotx_rounded) + ' ,' + str(asset_roty_rounded) + ' ,' + str(asset_rotz_rounded))
                    xform_report[transform].append(report_list)
                if (asset_scalex != 1 or asset_scaley != 1 or asset_scalez != 1):
                    # Filling the list report for scale
                    if transform not in xform_report:
                        xform_report[transform] = []
                    report_list.append("<b style='color:rgb(255,0,0);'>Freeze Transform failed:</b> " + 'Object ' + str(transform) + ' scale ' + 'is: ' + str(asset_scalex_rounded) + ' ,' + str(asset_scaley_rounded) + ' ,' + str(asset_scalez_rounded))
                    xform_report[transform].append(report_list)
            else:
                status_flag = 'passed'
        
    # Running the fix
    elif button_clicked == 'fix_button':
        # Initializing for the fix pass
        report_list = []
                
        # Performing rotate and scale xform
        for asset_mesh in polygon_meshes:
            transform = cmds.listRelatives(asset_mesh, parent=True)[0]
            attributes = [transform + ".rotateX", 
                          transform + ".rotateY", 
                          transform + ".rotateZ", 
                          transform + ".scaleX", 
                          transform + ".scaleY", 
                          transform + ".scaleZ"]

            failed_attributes = []
            
            for attr in attributes:
                # Checking if there are incoming connections
                connections = cmds.listConnections(attr, source=True, destination=False)
                if connections:
                   failed_attributes.append(attr)

            if failed_attributes:
                # Dictionary and list for the report
                xform_report = {}
                report_list = []

                # Check if rotation or scale are not zeroed out
                for asset_mesh in polygon_meshes:
                    transform = cmds.listRelatives(asset_mesh, parent=True)[0]

                    # Assigning rotation x, y z
                    asset_rotx = cmds.getAttr(transform + '.rotateX')
                    asset_roty = cmds.getAttr(transform + '.rotateY')
                    asset_rotz = cmds.getAttr(transform + '.rotateZ')

                    asset_rotx_rounded = round((asset_rotx), 2)
                    asset_roty_rounded = round((asset_roty), 2)
                    asset_rotz_rounded = round((asset_rotz), 2)

                    # Assigning scale x, y z
                    asset_scalex = cmds.getAttr(transform + '.scaleX')
                    asset_scaley = cmds.getAttr(transform + '.scaleY')
                    asset_scalez = cmds.getAttr(transform + '.scaleZ')

                    asset_scalex_rounded = round((asset_scalex), 2)
                    asset_scaley_rounded = round((asset_scaley), 2)
                    asset_scalez_rounded = round((asset_scalez), 2)

                    # If there's values
                    if (asset_rotx != 0 or asset_roty != 0 or asset_rotz != 0) or (asset_scalex != 1 or asset_scaley != 1 or asset_scalez != 1):
                        # Check has failed
                        status_flag = 'failed'

                        # Filling the list report
                        if asset_rotx != 0 or asset_roty != 0 or asset_rotz != 0:
                            # Filling the report for rotation
                            if transform not in xform_report:
                                xform_report[transform] = []
                            report_list.append("<b style='color:rgb(255,0,0);'>Freeze Transform failed:</b> " + 'Object ' + str(transform) + ' rotation ' + 'is: ' + str(asset_rotx_rounded) + ' ,' + str(asset_roty_rounded) + ' ,' + str(asset_rotz_rounded))
                            xform_report[transform].append(report_list)
                        if (asset_scalex != 1 or asset_scaley != 1 or asset_scalez != 1):
                            # Filling the list report for scale
                            if transform not in xform_report:
                                xform_report[transform] = []
                            report_list.append("<b style='color:rgb(255,0,0);'>Freeze Transform failed:</b> " + 'Object ' + str(transform) + ' scale ' + 'is: ' + str(asset_scalex_rounded) + ' ,' + str(asset_scaley_rounded) + ' ,' + str(asset_scalez_rounded))
                            xform_report[transform].append(report_list)

                # Putting the button_switch to 1, to trick the creation report NOT to empty the report because here, the xform will not perform
                button_switch = 1

                # Creating a message for incoming connections issue
                message = "Couldn't freeze transform on '" + transform + "' due to incoming connections. Run the 'Animated Objects' check pass before this one."
                cmds.confirmDialog(title='Error', message=message, button=['Ok'])
                status_flag = 'failed'
                continue
            else:
                # Performing the freeze transforms
                cmds.makeIdentity(transform, apply=True, rotate=True, scale=True, normal=0, preserveNormals=1)
                xform_report = {}
                status_flag = 'passed'
    
    return (status_flag,
            xform_report,
            button_switch
            )
