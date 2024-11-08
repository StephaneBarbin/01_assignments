# **************************************************************************************************************
# content       = increment save (for now)
#
# how to        =
# dependencies  = Maya
# to dos        =
#
# author  = Stephane Barbin
# **************************************************************************************************************



import os

import maya.cmds as cmds



# **************************************************************************************************************



def increment_version_scene():
    
    open_file_path = cmds.file(query=True, sceneName=True)

    # If not saved
    if not open_file_path:
        message = 'Scene needs to be saved'
        cmds.confirmDialog(title='Warning', message=message, button=['Ok'])
        return

    # Split path
    file_name, extension = os.path.splitext(open_file_path)
    split_name = file_name.split('_')

    old_version = ''

    # Search for vXXX
    for part in split_name:
        if part.startswith('v') and part[1:4].isdigit():
            old_version = part[1:]
            break

    if not old_version:
        message = 'No version found vXXX: ' + file_name
        cmds.confirmDialog(title='Warning', message=message, button=['Ok'])
        return

    new_version = int(old_version)
    new_version = new_version + 1
    new_version = 'v{:03}'.format(new_version)

    # Create new path
    new_file_path = open_file_path.replace('v' + old_version, new_version)

    # Save new file
    cmds.file(rename=new_file_path)
    cmds.file(save=True)
    
    message = 'Scene saved at: ' + str(new_file_path)
    cmds.confirmDialog(title='Saved', message=message, button=['Ok'])
    
    return new_file_path

