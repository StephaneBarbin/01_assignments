# DEMO TOOLS *********************************************************************
# content = menu & shelf
#
# date    = 2024-08-21
# author  = Stephane Barbin
#******************************************************************************

# Importing modules
import maya.cmds as cmds
import importlib


# Initializing variables
MENU_NAME = 'Demo Tools'
IMG_PATH  = r"F:\_python\02_python_advanced\01_work\01_assignments\0_app\img"


# Menu
def custom_menu():
    delete_custom_menu()

    menu = cmds.menu(MENU_NAME, parent = 'MayaWindow', label = MENU_NAME, helpMenu = True, tearOff = True)

    
    # Submenu
    submenu = cmds.menuItem(parent = menu, subMenu = True, label='Assets')

    # QC Checks submenu
    cmds.menuItem(parent = submenu, label = 'QC Checks', command = 'import qc; qc.start()')

    # Documentation submenu
    cmds.menuItem(parent = submenu, label = 'Documentation', command = 'import webbrowser; webbrowser.open("file:///F:/_python/02_python_advanced/01_work/01_assignments/0_app/documents/Quality%20Control%20Checks%20Documentation.pdf")')


    # Break
    cmds.menuItem(parent = menu, divider = True)


# Delete menu if exists
def delete_custom_menu():
    if cmds.menu(MENU_NAME, query = True, exists = True):
        cmds.deleteUI(MENU_NAME, menu = True)



def shelf_button_command():
    reload_and_run('qc')



# Shelf
def custom_shelf():
    delete_custom_shelf()

    shelf = cmds.shelfLayout(MENU_NAME, parent = "ShelfLayout")

    icon_command = ('import importlib; '
                    'import qc; '
                    'importlib.reload(qc); '
                    'qc.start()')

    cmds.shelfButton(parent = shelf,
                     annotation = 'Asset Quality Control Checks',
                     image1 = IMG_PATH + "\checker.png",
                     command = icon_command)


# Delete shel if exists
def delete_custom_shelf():
    if cmds.shelfLayout(MENU_NAME, query = True, exists = True):
        cmds.deleteUI(MENU_NAME)
