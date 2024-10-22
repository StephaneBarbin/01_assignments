# Quality Control Checks *********************************************************************
# 
# This application runs a list of quality control checks, depending on the department,
# and shows the user a small report, explaining what checks failed and why, or shows a warning.
# The user can then decide to automatically fix the issues, run the checks again on selected
# ones or Publish the asset anyway.
#
# Wishlist: - Button "Publish" greyed-out unyil all department's checks are "passed"
#           - "Freeze Transform" report display could display differently
#           - Add a "Help" button in the ui to call the documentation
#           - Is the "Invert Selection" button necessary?
#           - Maybe a "Fix" button on the right of each checks that failed? Do we still need a
#           - "Fix All" button"?
#           - Fix double popups when running "Freeze Transform" while incoming connections
#           - Creating a module for the "gathering" of all mehes objects in the scene (since this tool
#              is based on the assumption that the production would only allow meshes objects to pass
#              the "modelling" qc checks, and the code is repeated in each check modules right now)
# 
# date    = 2024-08-30
# author  = Stephane Barbin
#*********************************************************************************************


# QUALITY CONTROL CHECKS MAIN
# ____________________________________________________________________________________________


# IMPORTING MODULES
import os
import sys
import importlib
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore

# UI
import qc_checks_ui
importlib.reload(qc_checks_ui)

# Modeling Center check
from qc_modules.modeling import modeling_center
importlib.reload(modeling_center)

# Modeling xform check
from qc_modules.modeling import modeling_xform
importlib.reload(modeling_xform)

# Modeling Scene Cleanup check
from qc_modules.modeling import modeling_scene_cleanup
importlib.reload(modeling_scene_cleanup)

# Modeling Animated Objects check
from qc_modules.modeling import modeling_animated_objects
importlib.reload(modeling_animated_objects)

# Modeling Publish action
from publishing_modules import save_increment
importlib.reload(save_increment)

# ____________________________________________________________________________________________


class QCChecks:
    def __init__(self):
        # Initializing
        self.status_flag = None
        self.passed_count = 0
        self.warning_count = 0
        self.failed_count = 0
        self.department_reports = {'Animated Objects'   : ({}, {'passed' : 0, 'warning' : 0, 'failed' : 0}),
                                   'Center'             : ({}, {'passed' : 0, 'warning' : 0, 'failed' : 0}),
                                   'Freeze Transform'   : ({}, {'passed' : 0, 'warning' : 0, 'failed' : 0}),
                                   'Scene Cleanup'      : ({}, {'passed' : 0, 'warning' : 0, 'failed' : 0})}

        # UI
        (self.wg_qcc, self.fix_this_btn, self.department_menu, 
         self.qc_list_widget, self.run_selected_btn, self.passed_label, 
         self.warning_label, self.failed_label, self.results_window,
         self.select_all_btn, self.select_none_btn, self.invert_selection_btn,
         self.publish_btn) = qc_checks_ui.qc_checks_ui()


        # Getting Maya main window as a QWidget
        maya_main_window_pointer = omui.MQtUtil.mainWindow()
        maya_main_window = wrapInstance(int(maya_main_window_pointer), QtWidgets.QWidget)

        # Parenting QC Checks UI to the Maya main window
        self.wg_qcc.setParent(maya_main_window)
        self.wg_qcc.setWindowFlags(QtCore.Qt.Window)

        
        # Button connections
        self.fix_this_btn.clicked.connect(lambda: self.department_selection('fix_button'))
        self.run_selected_btn.clicked.connect(lambda: self.department_selection('run_button'))
        self.qc_list_widget.itemClicked.connect(self.on_qc_list_clicked)
        self.select_all_btn.clicked.connect(self.report_output)
        self.select_none_btn.clicked.connect(self.report_output)
        self.invert_selection_btn.clicked.connect(self.report_output)
        self.publish_btn.clicked.connect(self.publish_the_scene)


        # Showing the UI
        self.wg_qcc.show()

    
    # Function to execute the report output if an item is selected
    def on_qc_list_clicked(self, item):
        # Check if the qc item is clicked
        self.report_output()


    # Function to generate the department reports (fill it or empty it)
    def department_reports_creation(self, report, button_switch, button_flag, item_text):
        if button_flag == 'run_button':
            if item_text == 'Animated Objects':
                self.department_reports['Animated Objects'] = (report, self.department_reports['Animated Objects'][1])
                self.report_output()
            elif item_text == 'Center':
                self.department_reports['Center'] = (report, self.department_reports['Center'][1])
                self.report_output()
            elif item_text == 'Freeze Transform':
                self.department_reports['Freeze Transform'] = (report, self.department_reports['Freeze Transform'][1])
                self.report_output()
            elif item_text == 'Scene Cleanup':
                self.department_reports['Scene Cleanup'] = (report, self.department_reports['Scene Cleanup'][1])
                self.report_output()
        elif button_flag == 'fix_button':
            if item_text == 'Animated Objects':
                self.department_reports['Animated Objects'] = ({}, self.department_reports['Animated Objects'][1])
                self.report_output()
            if item_text == 'Center':
                self.department_reports['Center'] = ({}, self.department_reports['Center'][1])
                self.report_output()
            elif item_text == 'Freeze Transform':
                if button_switch == 0:
                    self.department_reports['Freeze Transform'] = ({}, self.department_reports['Freeze Transform'][1])
                    self.report_output()
                else:
                    self.report_output()
            elif item_text == 'Scene Cleanup':
                self.department_reports['Scene Cleanup'] = ({}, self.department_reports['Scene Cleanup'][1])
                self.report_output()


    # Function to output the reports in the UI and change status labels
    def report_output(self):
        # Reseting the check counts
        self.passed_count = 0
        self.warning_count = 0
        self.failed_count = 0

        # Getting the report from the department report dictionary
        qc_items = self.qc_list_widget.selectedItems()
        self.results_window.clear()
        if qc_items:
            qc_items_names = []
            for selected in qc_items:
                qc_items_names.append(selected.text())
            for item in qc_items_names:
                for secondary_key in self.department_reports[item][0]:
                    report_string = '<br>'.join(self.department_reports[item][0][secondary_key][0])

                    # Output report in UI
                    self.results_window.append(report_string)
                    self.results_window.append('')

        # Getting the status counts
        for qc_cheks in self.department_reports.keys():
            if self.department_reports[qc_cheks][1]['passed'] == 1:
                self.passed_count += 1
            if self.department_reports[qc_cheks][1]['warning'] == 1:
                self.warning_count += 1
            if self.department_reports[qc_cheks][1]['failed'] == 1:
                self.failed_count += 1

        # Changing status labels in the UI
        self.passed_label.setText('Passed: ' + str(self.passed_count))
        self.warning_label.setText('Warning: ' + str(self.warning_count))
        self.failed_label.setText('Failed: ' + str(self.failed_count))


    def publish_the_scene(self):
        save_increment.increment_version_scene()


    # Function to choose which department's checklist to use
    def department_selection(self, button_flag):
        selected_department = self.department_menu.currentText()
        if selected_department == 'Modeling':
            self.modeling_checklist(button_flag)
        elif selected_department == 'Rigging':
            self.rigging_checklist(button_flag)
        elif selected_department == 'Animation':
            self.animation_checklist(button_flag)

    
   # Function for the modeling checklist
    def modeling_checklist(self, button_flag):
        # Going throught the selected checklist
        qc_items = self.qc_list_widget.selectedItems()
        for item in qc_items:
            if item.text() == 'Animated Objects':
                self.status_flag, self.animated_objects_report, self.button_switch = modeling_animated_objects.animated_objects(button_flag)
                modeling_animated_objects.animated_objects(button_flag)
                if self.status_flag == 'passed':
                    self.department_reports[item.text()][1]['passed'] = 1
                    self.department_reports[item.text()][1]['warning'] = 0
                    self.department_reports[item.text()][1]['failed'] = 0
                    self.department_reports_creation(self.animated_objects_report, self.button_switch, button_flag, item.text())
                elif self.status_flag == 'warning':
                    self.department_reports[item.text()][1]['passed'] = 0
                    self.department_reports[item.text()][1]['warning'] = 1
                    self.department_reports[item.text()][1]['failed'] = 0
                elif self.status_flag == 'failed':
                    self.department_reports[item.text()][1]['passed'] = 0
                    self.department_reports[item.text()][1]['warning'] = 0
                    self.department_reports[item.text()][1]['failed'] = 1
                    self.department_reports_creation(self.animated_objects_report, self.button_switch, button_flag, item.text())
            elif item.text() == 'Center':
                self.status_flag, self.center_report, self.button_switch = modeling_center.meshes_center(button_flag)
                modeling_center.meshes_center(button_flag)
                if self.status_flag == 'passed':
                    self.department_reports[item.text()][1]['passed'] = 1
                    self.department_reports[item.text()][1]['warning'] = 0
                    self.department_reports[item.text()][1]['failed'] = 0
                    self.department_reports_creation(self.center_report, self.button_switch, button_flag, item.text())
                elif self.status_flag == 'warning':
                    self.department_reports[item.text()][1]['passed'] = 0
                    self.department_reports[item.text()][1]['warning'] = 1
                    self.department_reports[item.text()][1]['failed'] = 0
                elif self.status_flag == 'failed':
                    self.department_reports[item.text()][1]['passed'] = 0
                    self.department_reports[item.text()][1]['warning'] = 0
                    self.department_reports[item.text()][1]['failed'] = 1
                    self.department_reports_creation(self.center_report, self.button_switch, button_flag, item.text())
            elif item.text() == 'Freeze Transform':
                self.status_flag, self.xform_report, self.button_switch = modeling_xform.meshes_xform(button_flag)
                modeling_xform.meshes_xform(button_flag)
                if self.status_flag == 'passed':
                    self.department_reports[item.text()][1]['passed'] = 1
                    self.department_reports[item.text()][1]['warning'] = 0
                    self.department_reports[item.text()][1]['failed'] = 0
                    self.department_reports_creation(self.xform_report, self.button_switch, button_flag, item.text())
                elif self.status_flag == 'warning':
                    self.department_reports[item.text()][1]['passed'] = 0
                    self.department_reports[item.text()][1]['warning'] = 1
                    self.department_reports[item.text()][1]['failed'] = 0
                elif self.status_flag == 'failed':
                    self.department_reports[item.text()][1]['passed'] = 0
                    self.department_reports[item.text()][1]['warning'] = 0
                    self.department_reports[item.text()][1]['failed'] = 1
                    self.department_reports_creation(self.xform_report, self.button_switch, button_flag, item.text())
            elif item.text() == 'Scene Cleanup':
                self.status_flag, self.cleanup_report, self.button_switch = modeling_scene_cleanup.illegal_cleanup(button_flag)
                modeling_scene_cleanup.illegal_cleanup(button_flag)
                if self.status_flag == 'passed':
                    self.department_reports[item.text()][1]['passed'] = 1
                    self.department_reports[item.text()][1]['warning'] = 0
                    self.department_reports[item.text()][1]['failed'] = 0
                    self.department_reports_creation(self.cleanup_report, self.button_switch, button_flag, item.text())
                elif self.status_flag == 'warning':
                    self.department_reports[item.text()][1]['passed'] = 0
                    self.department_reports[item.text()][1]['warning'] = 1
                    self.department_reports[item.text()][1]['failed'] = 0
                elif self.status_flag == 'failed':
                    self.department_reports[item.text()][1]['passed'] = 0
                    self.department_reports[item.text()][1]['warning'] = 0
                    self.department_reports[item.text()][1]['failed'] = 1
                    self.department_reports_creation(self.cleanup_report, self.button_switch, button_flag, item.text())
        


    # Function for the rigging checklist     
    def rigging_checklist(self):
        # Going throught the selected checklist
        qc_items = self.qc_list_widget.selectedItems()
        for item in qc_items:
            if item.text() == 'Animated Objects':
                pass
            elif item.text() == 'Control Shape Consistency':
                pass
            elif item.text() == 'Controllers Naming':
                pass
            elif item.text() == 'Joints Influence Count':
                pass
            elif item.text() == 'Joints Naming':
                pass
            elif item.text() == 'Layer Organization':
                pass
            elif item.text() == 'Scene Cleanup':
                pass


    # Function for the animation checklist
    def animation_checklist(self):
        # Going throught the selected checklist
        qc_items = self.qc_list_widget.selectedItems()
        for item in qc_items:
            if item.text() == 'In-Betweens':
                pass
            elif item.text() == 'Keyframe Analysis':
                pass
            elif item.text() == 'Layer Organization':
                pass
            elif item.text() == 'Redundant Keyframes':
                pass
            elif item.text() == 'Rigging Checks':
                pass
            elif item.text() == 'Scene Cleanup':
                pass


# Start the Quality Control Checks tool
def start():
    global main_widget
    main_widget = QCChecks()
