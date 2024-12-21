# **************************************************************************************************************
# content       = UI creation
#
# dependencies  = Maya
#
# author  = Stephane Barbin
# **************************************************************************************************************

import os
import yaml
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon, QDesktopServices


class QCCheckItemWidget(QtWidgets.QWidget):
    """
    A widget representing a Quality Check (QC) item in the UI.
    This widget is designed to display the name, status, and additional actions
    for a quality check. It includes:
        - A label for the check name.
        - A status indicator, which is color-coded.
        - A Fix button to trigger related actions.
        - A report button to display details.
    Attributes:
        check_name (str): The name of the QC check this widget represents.
        status_color (str): The color representing the current status of the QC check.
        fix_button (QtWidgets.QPushButton): A button to trigger actions to fix the check.
        report_button (QtWidgets.QPushButton): A button to display details.
    """
    def __init__(self, check_name, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui

        script_dir = os.path.dirname(os.path.abspath(__file__))
        fix_path = os.path.join(script_dir, '..', 'img', 'fix_icon.png')
        report_path = os.path.join(script_dir, '..', 'img', 'report_icon.png')

        self.setFixedHeight(30)

        # MAIN LAYOUT
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Check name and status indicator
        check_container = QtWidgets.QWidget()
        check_container_layout = QtWidgets.QHBoxLayout(check_container)
        check_container_layout.setContentsMargins(0, 0, 0, 0)
        check_container_layout.setSpacing(10)

        self.status_indicator = QtWidgets.QLabel()
        self.status_indicator.setFixedSize(18, 18)
        self.status_indicator.setStyleSheet('background-color: white; border-radius: 0px;')
        check_container_layout.addWidget(self.status_indicator, alignment=QtCore.Qt.AlignLeft)

        self.check_label = QtWidgets.QLabel(check_name)
        self.check_label.setFixedHeight(20)
        self.check_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        check_container_layout.addWidget(self.check_label, alignment=QtCore.Qt.AlignLeft)

        # Adding check_container to layout
        layout.addWidget(check_container, alignment=QtCore.Qt.AlignLeft)

        # BUTTONS
        # Fix button
        self.fix_button = QtWidgets.QPushButton()
        self.fix_button.setFixedSize(18, 18)
        self.fix_button.setIcon(QIcon(fix_path))
        self.fix_button.setToolTip('Click to fix this check')
        layout.addWidget(self.fix_button)

        # Report button
        self.report_button = QtWidgets.QPushButton()
        self.report_button.setFixedSize(18, 18)
        self.report_button.setIcon(QIcon(report_path))
        self.report_button.setToolTip('Click to show the report for this check')
        layout.addWidget(self.report_button)

        # Report button connection to display the reports
        self.report_button.clicked.connect(self.report_title)

    def set_status(self, color):
        # Updating the status color (white, green, red)
        self.status_indicator.setStyleSheet(f'background-color: {color}; border-radius: 0px;')

    def report_title(self):
        self.parent_ui.display_report(f'{self.check_label.text()}')



class QCChecksUI(QtWidgets.QWidget):
    """
    The main UI for performing Quality Checks (QC) in Maya.
    This class creates and manages the user interface for running QC checks
    and visualizing their statuses. It is designed to handle different departments
    (e.g., Modeling, Rigging) and allows users to run all checks, view individual
    check results, and access additional actions for specific checks.

    Attributes:
        - yml_departments (dict): Data from a YAML file containing departments
        and their associated QC checks.
        - yml_descriptions (dict): Descriptions for each QC check, loaded from
        a YAML file.
        - run_button (QtWidgets.QPushButton): A button to initiate the execution
        of all QC checks.
        - processing_label (QtWidgets.QLabel): A label to display the progress or
        status of the QC process.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_dir = os.path.join(script_dir, "..", "data", "project")
    yml_departments = os.path.abspath(os.path.join(yaml_dir, 'departments.yml'))
    yml_descriptions = os.path.abspath(os.path.join(yaml_dir, 'descriptions.yml'))
    help_path = os.path.join(script_dir, "..", "img", "help_icon.png")

    def __init__(self):
        super().__init__()

        # Title and size
        self.setWindowTitle('Quality Control Checks')
        self.setGeometry(600, 200, 555, 700)

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        # Creating the dropdown list with 'departments' yaml configuration file
        with open(self.yml_departments, 'r') as stream:
            self.department_dropdown = yaml.load(stream, Loader=yaml.FullLoader)
        departments = list(self.department_dropdown.keys())

        combined_layout = QtWidgets.QHBoxLayout()
        combined_layout.setContentsMargins(0, 0, 0, 0)
        combined_layout.setSpacing(5)

        # Department dropdown menu
        self.department_menu = QtWidgets.QComboBox()
        self.department_menu.addItems(departments)
        self.department_menu.setToolTip('Click to select a department to run the checks')
        self.department_menu.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        combined_layout.addWidget(self.department_menu, stretch=1)

        spacer = QtWidgets.QSpacerItem(1, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        combined_layout.addItem(spacer)

        self.help_button = QtWidgets.QPushButton()
        self.help_button.setFixedSize(18, 18)
        self.help_button.setIcon(QIcon(self.help_path))
        self.help_button.setToolTip('Click to open the documentation.')
        combined_layout.addWidget(self.help_button, alignment=QtCore.Qt.AlignRight)
        self.help_button.clicked.connect(self.help_page)

        # Adding combined_layout to main_layout
        self.main_layout.addLayout(combined_layout)

        # Splitter to separate check and report area
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)

        # Check area
        self.check_layout = QtWidgets.QVBoxLayout()
        self.check_layout.setSpacing(5)
        self.check_layout.setAlignment(QtCore.Qt.AlignTop)

        self.checks_widget = QtWidgets.QWidget()
        self.checks_widget.setLayout(self.check_layout)

        self.check_area = QtWidgets.QScrollArea()
        self.check_area.setWidget(self.checks_widget)
        self.check_area.setWidgetResizable(True)

        self.splitter.addWidget(self.check_area)

        # Description area
        self.description_area = QtWidgets.QTextEdit()
        self.description_area.setReadOnly(True)
        self.description_area.setVisible(False)
        self.splitter.addWidget(self.description_area)

        # Report area
        self.report_area = QtWidgets.QTextEdit()
        self.report_area.setReadOnly(True)
        self.report_area.setVisible(False)
        self.splitter.addWidget(self.report_area)

        self.splitter.setSizes([300, 150, 150])

        # Add splitter to main_layout
        self.main_layout.addWidget(self.splitter)

        # Processing label and Run button
        combined_layout = QtWidgets.QHBoxLayout()
        combined_layout.setContentsMargins(0, 0, 0, 0)
        combined_layout.setSpacing(10)

        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setToolTip('Displays the QC tool current state')
        self.status_label.setAlignment(QtCore.Qt.AlignVCenter)
        combined_layout.addWidget(self.status_label, alignment=QtCore.Qt.AlignLeft)

        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        combined_layout.addItem(spacer)

        self.run_button = QtWidgets.QPushButton('Run')
        self.run_button.setFixedWidth(100)
        self.run_button.setToolTip('Click to run all quality control checks.')
        self.run_button.clicked.connect(self.toggle_area)
        combined_layout.addWidget(self.run_button, alignment=QtCore.Qt.AlignRight)

        # Add combined_layout to main_layout
        self.main_layout.addLayout(combined_layout)

        self.file_department_set()
        self.load_check()

        # Parenting UI to Maya main window
        maya_main_window_pointer = omui.MQtUtil.mainWindow()
        maya_main_window = wrapInstance(int(maya_main_window_pointer), QtWidgets.QWidget)
        self.setParent(maya_main_window)
        self.setWindowFlags(QtCore.Qt.Window)


    def file_department_set(self):
        """
        Setting initial dropdown menu selection to correspond to the opened file
        """
        scene_path = cmds.file(query=True, sceneName=True)
        file_name = os.path.basename(scene_path)

        if file_name:
            if file_name.startswith('mdl'):
                self.department_menu.setCurrentIndex(0)
            elif file_name.startswith('rig'):
                self.department_menu.setCurrentIndex(1)
            elif file_name.startswith('ani'):
                self.department_menu.setCurrentIndex(2)
            else:
                pass
        else:
            message = "Scene is Untitled. Department dropdown will be set to the first choice by default. Please save your scene with the proper department prefix"
            cmds.confirmDialog(title='Warning', message=message, button=['Ok'])
            pass


    def load_check(self):
        """
        Populating the checks with the use of a 'departments.yml' file.
        """
        for index in reversed(range(self.check_layout.count())):
            widget = self.check_layout.takeAt(index).widget()
            if widget:
                widget.deleteLater()

        department = self.department_menu.currentText()

        # Creating the department list with 'departments' yaml configuration file
        with open(self.yml_departments, 'r') as stream:
            self.checks = yaml.load(stream, Loader=yaml.FullLoader)

        # Populating checks in a dictionary
        self.check_widgets = {}
        for check in self.checks.get(department, []):
            check_widget = QCCheckItemWidget(check, self)
            self.check_layout.addWidget(check_widget)
            self.check_widgets[check] = check_widget

    def display_report(self, details_text):
        """
        Displaying the report for failed check.

        Args:
            details_text (str): The text to display in the details area.
        """
        self.check_area.setVisible(False)
        self.description_area.setVisible(True)
        self.report_area.setVisible(True)
        self.department_menu.setEnabled(False)

        formatted_text = self.display_description(details_text)

        self.description_area.setHtml(formatted_text)

        self.run_button.setText("Back")
        self.run_button.setToolTip('Click to return to the check list page.')

    def display_description(self, details_text):
        """
        Retrieving and displaying the description for a given check name from the 'descriptions.yml' file.

        Args:
            details_text (str): The name of the check to retrieve the description for.
        Returns:
            str: The formatted HTML content with the check name and its description.
        """
        with open(self.yml_descriptions, 'r') as stream:
            self.descriptions = yaml.load(stream, Loader=yaml.FullLoader)

        department = self.department_menu.currentText()

        # Get the description from 'descriptions.yml'
        description_lines = self.descriptions.get(department, {}).get(details_text, [])

        if description_lines:
            description = "<br>".join(description_lines)

        formatted_text = f"""<p><b style="font-size:18px;">{details_text}</b></p>
                             <p><br></p>
                             <p style="font-size:12px; font-weight:normal;">{description}</p>"""

        return formatted_text

    def scene_report(self, report_string):
        """
        Displaying the scene report details in the report area.

        Args:
            report_string (str): The report content to display.
        """
        self.check_area.setVisible(False)
        self.description_area.setVisible(True)
        self.report_area.setVisible(True)
        self.report_area.setHtml(report_string)

    def toggle_area(self):
        """
            Toggling between the checks and the report 'page'.
        """
        if self.description_area.isVisible() and self.report_area.isVisible():
            self.description_area.setVisible(False)
            self.report_area.setVisible(False)
            self.check_area.setVisible(True)
            self.department_menu.setEnabled(True)

        else:
            self.description_area.setVisible(False)
            self.report_area.setVisible(False)
            self.check_area.setVisible(True)

        self.report_area.clear()

    def update_status_color(self, check_name, status):
        """
        Updating the status indicator color for a given check.

        Args:
            check_name (str): Name of the check being updated.
            status (str): The result of the check ('passed', 'failed', etc.).
        """
        color = {'passed':  'green',
                 'failed':  'red',
                 'warning': 'yellow',
                }.get(status, 'gray')  # Default to gray if status is unknown

        check_widget = self.check_widgets.get(check_name)
        if check_widget:
            check_widget.set_status(color)

    def get_checks(self):
        """
        Returns the 'checks' dictionary for use in the 'qc.py' main module.
        """
        return self.checks

    def help_page(self):
        """
        Opening the help webpage in the default browser.
        """
        help_url = QtCore.QUrl("https://github.com/StephaneBarbin/01_assignments/wiki")
        if not QDesktopServices.openUrl(help_url):
            print("Failed to open the help URL.")


if __name__ == '__main__':
    window = QCChecksUI()
    window.show()
