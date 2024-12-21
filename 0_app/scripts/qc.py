# **************************************************************************************************************
# content       = loads qc check's UI
#
# how to        = start()
# dependencies  = Maya
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

from scripts import qc_ui
importlib.reload(qc_ui)

from checks.modeling import modeling_center
importlib.reload(modeling_center)

from checks.modeling import modeling_xform
importlib.reload(modeling_xform)

from checks.modeling import modeling_scene_cleanup
importlib.reload(modeling_scene_cleanup)

from checks.modeling import modeling_animated_objects
importlib.reload(modeling_animated_objects)

from checks import save_increment
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
        self.modeling_reports = {'Animated Objects':          ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Center':                    ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Freeze Transform':          ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Scene Cleanup':             ({}, {'passed': 0, 'warning': 0, 'failed': 0})}
        self.rigging_reports = {'Animated Objects':           ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Control Shape Consistency': ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Controllers Naming':        ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Joints Influence Count':    ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Layer Organization':        ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Scene Cleanup':             ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                 'Joints Naming':             ({}, {'passed': 0, 'warning': 0, 'failed': 0})}
        self.animation_reports = {'Keyframe Analysis':        ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                  'In-Betweens':              ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                  'Rigging Checks':           ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                  'Redundant Keyframes':      ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                  'Scene Cleanup':            ({}, {'passed': 0, 'warning': 0, 'failed': 0}),
                                  'Layer Organization':       ({}, {'passed': 0, 'warning': 0, 'failed': 0})}

        self.publish_button = 0

        # Creating the QCChecksUI instance and show the UI
        self.qc_ui = qc_ui.QCChecksUI()
        self.qc_ui.show()

        # Button connections
        def button_condition():
            if self.qc_ui.run_button.text() == 'Run':
                self.action = 'fix_pass'
                self.department_selection('run_button', 'all')
            elif self.qc_ui.run_button.text() == 'Back':
                if self.publish_button == 1:
                    self.qc_ui.run_button.setText('Publish')
                    self.qc_ui.run_button.setToolTip('Click to publish the scene.')
                else:
                    self.qc_ui.run_button.setText('Run')
                    self.qc_ui.run_button.setToolTip('Click to run all quality control checks.')
            elif self.qc_ui.run_button.text() == 'Publish':
                self.publish_the_scene()
        self.qc_ui.run_button.clicked.connect(button_condition)
        self.qc_ui.department_menu.currentIndexChanged.connect(self.update_button_connection)
        for check_name, check_widget in self.qc_ui.check_widgets.items():
            check_widget.report_button.clicked.connect(lambda _=None, chk_name = check_name: self.show_report(chk_name))
        for check_name, check_widget in self.qc_ui.check_widgets.items():
            check_widget.fix_button.clicked.connect(lambda _=None, chk_name = check_name: self.department_selection('fix_button', chk_name))


    def department_selection(self, button_flag, check):
        """
        Choosing which department's checklist to use
        """
        selected_department = self.qc_ui.department_menu.currentText()
        if selected_department == 'Modeling':
            self.modeling_checklist(button_flag, check)
        elif selected_department == 'Rigging':
            self.rigging_checklist(button_flag, check)
        elif selected_department == 'Animation':
            self.animation_checklist(button_flag, check)


    def update_button_connection(self):
        """
        Updating the report button connection when department dropdown selection changes.
        """
        for check_widget in self.qc_ui.check_widgets.values():
            try:
                check_widget.report_button.clicked.disconnect()
                check_widget.fix_button.clicked.disconnect()
            except TypeError:
                pass

        self.qc_ui.load_check()

        for check_name, check_widget in self.qc_ui.check_widgets.items():
            check_widget.report_button.clicked.connect(lambda _=None, chk_name=check_name: self.show_report(chk_name))
        for check_name, check_widget in self.qc_ui.check_widgets.items():
            check_widget.fix_button.clicked.connect(lambda _=None, chk_name = check_name: self.department_selection('fix_button', chk_name))


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

    # MODELING CHECKS

    @processing_status
    def modeling_checklist(self, button_flag, check):
        """
        Performing the Modeling checks or fixing them

        Args:
            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'
            check (str): Contains the name of the quality check
        """
        checks = self.qc_ui.get_checks()
        if button_flag == 'run_button':
            for item in checks['Modeling']:
                if item == 'Animated Objects':
                    self.animated_objects(button_flag)
                elif item == 'Center':
                    self.center(button_flag)
                elif item == 'Freeze Transform':
                    self.freeze_transform(button_flag)
                elif item == 'Scene Cleanup':
                    self.scene_cleanup(button_flag)
        elif button_flag == 'fix_button':
            if check == 'Animated Objects':
                self.animated_objects(button_flag)
            elif check == 'Center':
                self.center(button_flag)
            elif check == 'Freeze Transform':
                self.freeze_transform(button_flag)
            elif check == 'Scene Cleanup':
                self.scene_cleanup(button_flag)
        if self.all_passed():
            self.publish_button = 1
            self.qc_ui.run_button.setText('Publish')
            self.qc_ui.run_button.setToolTip('Click to publish the scene.')
        else:
            self.publish_button = 0


    def animated_objects(self, button_flag):
        """
        Performing the Animated Objects checks

        Args:
            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'
        """
        item = 'Animated Objects'
        self.status_flag, self.animated_objects_report, self.button_switch = modeling_animated_objects.animated_objects(
            button_flag)
        modeling_animated_objects.animated_objects(button_flag)
        if self.status_flag == 'passed':
            self.modeling_reports[item][1]['passed'] = 1
            self.modeling_reports[item][1]['warning'] = 0
            self.modeling_reports[item][1]['failed'] = 0
            self.department_reports_creation(self.animated_objects_report, self.button_switch, button_flag, item)
        elif self.status_flag == 'warning':
            self.modeling_reports[item][1]['passed'] = 0
            self.modeling_reports[item][1]['warning'] = 1
            self.modeling_reports[item][1]['failed'] = 0
        elif self.status_flag == 'failed':
            self.modeling_reports[item][1]['passed'] = 0
            self.modeling_reports[item][1]['warning'] = 0
            self.modeling_reports[item][1]['failed'] = 1
            self.department_reports_creation(self.animated_objects_report, self.button_switch, button_flag, item)

    def center(self, button_flag):
        """
        Performing the Center checks

        Args:
            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'
        """
        item = 'Center'
        self.status_flag, self.center_report, self.button_switch = modeling_center.meshes_center(button_flag)
        modeling_center.meshes_center(button_flag)
        if self.status_flag == 'passed':
            self.modeling_reports[item][1]['passed'] = 1
            self.modeling_reports[item][1]['warning'] = 0
            self.modeling_reports[item][1]['failed'] = 0
            self.department_reports_creation(self.center_report, self.button_switch, button_flag, item)
        elif self.status_flag == 'warning':
            self.modeling_reports[item][1]['passed'] = 0
            self.modeling_reports[item][1]['warning'] = 1
            self.modeling_reports[item][1]['failed'] = 0
        elif self.status_flag == 'failed':
            self.modeling_reports[item][1]['passed'] = 0
            self.modeling_reports[item][1]['warning'] = 0
            self.modeling_reports[item][1]['failed'] = 1
            self.department_reports_creation(self.center_report, self.button_switch, button_flag, item)

    def freeze_transform(self, button_flag):
        """
        Performing the Freeze Transform checks

        Args:
            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'
        """
        item = 'Freeze Transform'
        self.status_flag, self.xform_report, self.button_switch = modeling_xform.meshes_xform(button_flag)
        modeling_xform.meshes_xform(button_flag)
        if self.status_flag == 'passed':
            self.modeling_reports[item][1]['passed'] = 1
            self.modeling_reports[item][1]['warning'] = 0
            self.modeling_reports[item][1]['failed'] = 0
            self.department_reports_creation(self.xform_report, self.button_switch, button_flag, item)
        elif self.status_flag == 'warning':
            self.modeling_reports[item][1]['passed'] = 0
            self.modeling_reports[item][1]['warning'] = 1
            self.modeling_reports[item][1]['failed'] = 0
        elif self.status_flag == 'failed':
            self.modeling_reports[item][1]['passed'] = 0
            self.modeling_reports[item][1]['warning'] = 0
            self.modeling_reports[item][1]['failed'] = 1
            self.department_reports_creation(self.xform_report, self.button_switch, button_flag, item)

    def scene_cleanup(self, button_flag):
        """
        Performing the Center checks

        Args:
            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'
        """
        item = 'Scene Cleanup'
        self.status_flag, self.cleanup_report, self.button_switch = modeling_scene_cleanup.illegal_cleanup(button_flag)
        modeling_scene_cleanup.illegal_cleanup(button_flag)
        if self.status_flag == 'passed':
            self.modeling_reports[item][1]['passed'] = 1
            self.modeling_reports[item][1]['warning'] = 0
            self.modeling_reports[item][1]['failed'] = 0
            self.department_reports_creation(self.cleanup_report, self.button_switch, button_flag, item)
        elif self.status_flag == 'warning':
            self.modeling_reports[item][1]['passed'] = 0
            self.modeling_reports[item][1]['warning'] = 1
            self.modeling_reports[item][1]['failed'] = 0
        elif self.status_flag == 'failed':
            self.modeling_reports[item][1]['passed'] = 0
            self.modeling_reports[item][1]['warning'] = 0
            self.modeling_reports[item][1]['failed'] = 1
            self.department_reports_creation(self.cleanup_report, self.button_switch, button_flag, item)


    # RIGGING CHECKS

    def rigging_checklist(self, button_flag, check):
        """
        Performing the Rigging checklist

        Args:
            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'
            check (str): Contains the name of the quality check
        """
        print('Rigging Checks')


    # ANIMATION CHECKS *************************************************************************************************

    def animation_checklist(self, button_flag, check):
        """
        Performing the Animation checklist

        Args:
            button_flag (str): Contains info on the button pressed i.e.: 'Run' or 'Fix'
            check (str): Contains the name of the quality check
        """
        print('Animation Checks')


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
                self.modeling_reports['Animated Objects'] = (report, self.modeling_reports['Animated Objects'][1])
                self.qc_ui.update_status_color('Animated Objects', self.status_flag)
            elif item_text == 'Center':
                self.modeling_reports['Center'] = (report, self.modeling_reports['Center'][1])
                self.qc_ui.update_status_color('Center', self.status_flag)
            elif item_text == 'Freeze Transform':
                self.modeling_reports['Freeze Transform'] = (report, self.modeling_reports['Freeze Transform'][1])
                self.qc_ui.update_status_color('Freeze Transform', self.status_flag)
            elif item_text == 'Scene Cleanup':
                self.modeling_reports['Scene Cleanup'] = (report, self.modeling_reports['Scene Cleanup'][1])
                self.qc_ui.update_status_color('Scene Cleanup', self.status_flag)
        elif button_flag == 'fix_button':
            if item_text == 'Animated Objects':
                self.modeling_reports['Animated Objects'] = ({}, self.modeling_reports['Animated Objects'][1])
                self.qc_ui.update_status_color('Animated Objects', self.status_flag)
            if item_text == 'Center':
                self.modeling_reports['Center'] = ({}, self.modeling_reports['Center'][1])
                self.qc_ui.update_status_color('Center', self.status_flag)
            elif item_text == 'Freeze Transform':
                if button_switch == 0:
                    self.modeling_reports['Freeze Transform'] = ({}, self.modeling_reports['Freeze Transform'][1])
                    self.qc_ui.update_status_color('Freeze Transform', self.status_flag)
                else:
                    self.qc_ui.update_status_color('Freeze Transform', self.status_flag)
            elif item_text == 'Scene Cleanup':
                self.modeling_reports['Scene Cleanup'] = ({}, self.modeling_reports['Scene Cleanup'][1])
                self.qc_ui.update_status_color('Scene Cleanup', self.status_flag)


    def show_report(self, check):
        """
        Displaying the report for a giving check

        Args:
            check (str): Contains the name of the quality check
        """
        report_string = ""
        selected_department = self.qc_ui.department_menu.currentText()
        if selected_department == 'Modeling':
            if self.modeling_reports[check][0]:
                for secondary_key in self.modeling_reports[check][0]:
                    report_string = '<br>'.join(self.modeling_reports[check][0][secondary_key][0])
                    self.qc_ui.scene_report(report_string)
            else:
                report_string = "No errors"
                self.qc_ui.scene_report(report_string)
        elif selected_department == 'Rigging':
            if self.rigging_reports[check][0]:
                for secondary_key in self.rigging_reports[check][0]:
                    report_string = '<br>'.join(self.rigging_reports[check][0][secondary_key][0])
                    self.qc_ui.scene_report(report_string)
            else:
                report_string = "No errors"
                self.qc_ui.scene_report(report_string)
        elif selected_department == 'Animation':
            if self.animation_reports[check][0]:
                for secondary_key in self.animation_reports[check][0]:
                    report_string = '<br>'.join(self.animation_reports[check][0][secondary_key][0])
                    self.qc_ui.scene_report(report_string)
            else:
                report_string = "No errors"
                self.qc_ui.scene_report(report_string)

    def all_passed(self):
        """
        Verify if all checks have passed in order to change the 'Run' button to 'Publish'
        """
        for status_dict in self.modeling_reports.values():
            if status_dict[1]['passed'] != 1:
                return False
        return True


    def publish_the_scene(self):
        """
        Save increment the scene
        """
        save_increment.increment_version_scene()


def start():
    """
    Start the Quality Control Checks tool
    """
    global main_widget
    main_widget = QCChecks()
