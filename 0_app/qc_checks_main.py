# **************************************************************************************************************
# content       = loads qc check's UI
#
# how to        = start()
# dependencies  = Maya
# to dos        = Add 'Report' output, add "Fix" button
#                 Fix double popups when running "Freeze Transform" while incoming connections
#
# author  = Stephane Barbin
# **************************************************************************************************************


import os
import sys
import importlib
import maya.OpenMayaUI as omUI
from shiboken2 import wrapInstance

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets

import qcc_ui
importlib.reload(qcc_ui)

from qc_modules.modeling import modeling_center
importlib.reload(modeling_center)

from qc_modules.modeling import modeling_xform
importlib.reload(modeling_xform)

from qc_modules.modeling import modeling_scene_cleanup
importlib.reload(modeling_scene_cleanup)

from qc_modules.modeling import modeling_animated_objects
importlib.reload(modeling_animated_objects)

from publishing_modules import save_increment
importlib.reload(save_increment)



# **************************************************************************************************************



class QCChecks:
    """
    This is the main Quality Control Checks, performed by department users.
    It gives the user the ability to see a report based on checks that fails, select
    the checks they want to resolve automatically and "Publish" when all checks are "passed".
    """
    def __init__(self):
        """
        Initializing
        """
        self.status_flag = None
        self.passed_count = 0
        self.warning_count = 0
        self.failed_count = 0
        self.department_reports = {'Animated Objects': ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                   'Center':           ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                   'Freeze Transform': ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                   'Scene Cleanup':    ({}, {'passed': 0, 'warning': 0, 'failed': 0})}

        # Creating the QCChecksUI instance and show the UI
        self.qc_ui = qcc_ui.QCChecksUI()
        self.qc_ui.show()

        # Button connections
        self.qc_ui.run_all_btn.clicked.connect(lambda: self.department_selection('run_button'))


    def department_selection(self, button_flag):
        """
        Choosing which department's checklist to use
        """
        selected_department = self.qc_ui.department_menu.currentText()
        if selected_department == 'Modeling':
            self.modeling_checklist(button_flag)
        elif selected_department == 'Rigging':
            self.rigging_checklist(button_flag)
        elif selected_department == 'Animation':
            self.animation_checklist(button_flag)

    def processing_status(func):
        """
        Decorator to update the status text in the UI while a function is running.
        """
        def wrapper(self, *args, **kwargs):
            self.qc_ui.status_label.setText("Processing...")
            QtWidgets.QApplication.processEvents()
            result = func(self, *args, **kwargs)
            self.qc_ui.status_label.setText("Ready")
            return result
        return wrapper

    @processing_status
    def modeling_checklist(self, button_flag):
        """
        Performing the Modeling checklist

        Args:
            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'
        """
        checks = self.qc_ui.get_checks()
        for item in checks['Modeling']:
            if item == 'Animated Objects':
                self.status_flag, self.animated_objects_report, self.button_switch = modeling_animated_objects.animated_objects(button_flag)
                modeling_animated_objects.animated_objects(button_flag)
                if self.status_flag == 'passed':
                    self.department_reports[item][1]['passed'] = 1
                    self.department_reports[item][1]['warning'] = 0
                    self.department_reports[item][1]['failed'] = 0
                    self.department_reports_creation(self.animated_objects_report, self.button_switch, button_flag, item)
                elif self.status_flag == 'warning':
                    self.department_reports[item][1]['passed'] = 0
                    self.department_reports[item][1]['warning'] = 1
                    self.department_reports[item][1]['failed'] = 0
                elif self.status_flag == 'failed':
                    self.department_reports[item][1]['passed'] = 0
                    self.department_reports[item][1]['warning'] = 0
                    self.department_reports[item][1]['failed'] = 1
                    self.department_reports_creation(self.animated_objects_report, self.button_switch, button_flag, item)
            elif item == 'Center':
                self.status_flag, self.center_report, self.button_switch = modeling_center.meshes_center(button_flag)
                modeling_center.meshes_center(button_flag)
                if self.status_flag == 'passed':
                    self.department_reports[item][1]['passed'] = 1
                    self.department_reports[item][1]['warning'] = 0
                    self.department_reports[item][1]['failed'] = 0
                    self.department_reports_creation(self.center_report, self.button_switch, button_flag, item)
                elif self.status_flag == 'warning':
                    self.department_reports[item][1]['passed'] = 0
                    self.department_reports[item][1]['warning'] = 1
                    self.department_reports[item][1]['failed'] = 0
                elif self.status_flag == 'failed':
                    self.department_reports[item][1]['passed'] = 0
                    self.department_reports[item][1]['warning'] = 0
                    self.department_reports[item][1]['failed'] = 1
                    self.department_reports_creation(self.center_report, self.button_switch, button_flag, item)
            elif item == 'Freeze Transform':
                self.status_flag, self.xform_report, self.button_switch = modeling_xform.meshes_xform(button_flag)
                modeling_xform.meshes_xform(button_flag)
                if self.status_flag == 'passed':
                    self.department_reports[item][1]['passed'] = 1
                    self.department_reports[item][1]['warning'] = 0
                    self.department_reports[item][1]['failed'] = 0
                    self.department_reports_creation(self.xform_report, self.button_switch, button_flag, item)
                elif self.status_flag == 'warning':
                    self.department_reports[item][1]['passed'] = 0
                    self.department_reports[item][1]['warning'] = 1
                    self.department_reports[item][1]['failed'] = 0
                elif self.status_flag == 'failed':
                    self.department_reports[item][1]['passed'] = 0
                    self.department_reports[item][1]['warning'] = 0
                    self.department_reports[item][1]['failed'] = 1
                    self.department_reports_creation(self.xform_report, self.button_switch, button_flag, item)
            elif item == 'Scene Cleanup':
                self.status_flag, self.cleanup_report, self.button_switch = modeling_scene_cleanup.illegal_cleanup(
                    button_flag)
                modeling_scene_cleanup.illegal_cleanup(button_flag)
                if self.status_flag == 'passed':
                    self.department_reports[item][1]['passed'] = 1
                    self.department_reports[item][1]['warning'] = 0
                    self.department_reports[item][1]['failed'] = 0
                    self.department_reports_creation(self.cleanup_report, self.button_switch, button_flag, item)
                elif self.status_flag == 'warning':
                    self.department_reports[item][1]['passed'] = 0
                    self.department_reports[item][1]['warning'] = 1
                    self.department_reports[item][1]['failed'] = 0
                elif self.status_flag == 'failed':
                    self.department_reports[item][1]['passed'] = 0
                    self.department_reports[item][1]['warning'] = 0
                    self.department_reports[item][1]['failed'] = 1
                    self.department_reports_creation(self.cleanup_report, self.button_switch, button_flag, item)


    def rigging_checklist(self):
        """
        Performing the Rigging checklist
        """
        qc_items = self.qc_list_widget.selectedItems()
        for item in qc_items:
            if item == 'Animated Objects':
                pass
            elif item == 'Control Shape Consistency':
                pass
            elif item == 'Controllers Naming':
                pass
            elif item == 'Joints Influence Count':
                pass
            elif item == 'Joints Naming':
                pass
            elif item == 'Layer Organization':
                pass
            elif item == 'Scene Cleanup':
                pass


    def animation_checklist(self):
        """
        Performing the Animation checklist for what the user have selected
        """
        qc_items = self.qc_list_widget.selectedItems()
        for item in qc_items:
            if item == 'In-Betweens':
                pass
            elif item == 'Keyframe Analysis':
                pass
            elif item == 'Layer Organization':
                pass
            elif item == 'Redundant Keyframes':
                pass
            elif item == 'Rigging Checks':
                pass
            elif item == 'Scene Cleanup':
                pass


    def department_reports_creation(self, report, button_switch, button_flag, item_text):
        """
        Generate the department reports (fill it or empty it)

        Args:
            report (dict[str, tuple[dict, dict[str, int]] | tuple[TypedDict, dict[str, int]]]):
            A dictionary where the keys are the checks in the checklist (str) and the values are tuples.
            Each tuple can contain:
            - A generic dictionary and a dictionary with string keys and integer values.
            - A TypedDict and a dictionary with string keys and integer values.
            In summary, the check to be performed, its result from the module to be displayed to the user
            and information as to if the check has passed, failed or is a warning

            button_switch (int): A flag that comes from outside modules, that tells if the check passes or not

            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'

            item_text (str): Contains the name of the actual check from the checklist
        """
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


    def report_output(self):
        """
        Output the reports in the UI and change status labels
        """
        # Resetting the check counts
        self.passed_count = 0
        self.warning_count = 0
        self.failed_count = 0
        # Getting the report from the department report dictionary
        qc_items = self.qc_ui.get_checks()
        for item in qc_items['Modeling']:
            for secondary_key in self.department_reports[item][0]:
                report_string = '<br>'.join(self.department_reports[item][0][secondary_key][0])
                # Output report in UI
                #self.results_window.append(report_string)
                #self.results_window.append('')
            self.qc_ui.update_status_color(item, self.status_flag)


    def publish_the_scene(self):
        save_increment.increment_version_scene()


def start():
    """
    Start the Quality Control Checks tool
    """
    global main_widget
    main_widget = QCChecks()
