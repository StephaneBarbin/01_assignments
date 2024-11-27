# **************************************************************************************************************
# content       = UI creation
#
# dependencies  = Maya
#
# author  = Stephane Barbin
# **************************************************************************************************************

import yaml
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore, QtGui


class QCCheckItemWidget(QtWidgets.QWidget):
    def __init__(self, check_name):
        super().__init__()

        self.setFixedHeight(30)

        # Main layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)

        # status indicator and check name
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QHBoxLayout(container)
        container_layout.setContentsMargins(215, 0, 0, 0)  # Control horizontal start position
        container_layout.setSpacing(10)

        # Status color indicator
        self.status_indicator = QtWidgets.QLabel()
        self.status_indicator.setFixedSize(15, 15)
        self.status_indicator.setStyleSheet('background-color: white; border-radius: 0px;')
        container_layout.addWidget(self.status_indicator, alignment=QtCore.Qt.AlignLeft)

        # Check name label
        self.check_label = QtWidgets.QLabel(check_name)
        container_layout.addWidget(self.check_label, alignment=QtCore.Qt.AlignLeft)

        # Adding the container to the main layout
        layout.addWidget(container, alignment=QtCore.Qt.AlignLeft)

        # Arrow button for calling the report for fails
        self.arrow_button = QtWidgets.QPushButton('>')
        self.arrow_button.setFixedSize(15, 15)
        layout.addWidget(self.arrow_button, alignment=QtCore.Qt.AlignRight)

        # Temp report button connection
        self.arrow_button.clicked.connect(self.show_additional_options)

    def set_status(self, color):
        # Updating the status color (white, green, red)
        self.status_indicator.setStyleSheet(f'background-color: {color}; border-radius: 0px;')

    def show_additional_options(self):
        # Temp report
        print(f'Additional options for {self.check_label.text()}')


class QCChecksUI(QtWidgets.QWidget):
    yml_path = r"E:\departments.yml"

    def __init__(self):
        super().__init__()

        # Title and size
        self.setWindowTitle('Quality Control Checks')
        self.setGeometry(600, 200, 500, 700)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(15)  # Spacing between main layout items
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Department dropdown menu
        self.department_menu = QtWidgets.QComboBox()
        self.department_menu.addItems(['Modeling', 'Rigging', 'Animation'])
        self.department_menu.currentIndexChanged.connect(self.load_checks)
        main_layout.addWidget(self.department_menu)

        # CHECKS area
        self.checks_layout = QtWidgets.QVBoxLayout()
        self.checks_layout.setSpacing(0)
        self.checks_layout.setContentsMargins(15, 15, 15, 15)
        self.checks_layout.setAlignment(QtCore.Qt.AlignTop)

        self.checks_widget = QtWidgets.QWidget()
        self.checks_widget.setLayout(self.checks_layout)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.checks_widget)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        # PROCESSING label and RUN button
        combined_layout = QtWidgets.QHBoxLayout()
        combined_layout.setContentsMargins(0, 0, 0, 0)
        combined_layout.setSpacing(10)  # Space between widgets

        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setAlignment(QtCore.Qt.AlignVCenter)
        combined_layout.addWidget(self.status_label, alignment=QtCore.Qt.AlignLeft)

        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        combined_layout.addItem(spacer)

        self.run_all_btn = QtWidgets.QPushButton('Run')
        self.run_all_btn.setFixedWidth(100)
        combined_layout.addWidget(self.run_all_btn, alignment=QtCore.Qt.AlignRight)

        main_layout.addLayout(combined_layout)

        self.load_checks()

        # Parenting UI to Maya main window
        maya_main_window_pointer = omui.MQtUtil.mainWindow()
        maya_main_window = wrapInstance(int(maya_main_window_pointer), QtWidgets.QWidget)
        self.setParent(maya_main_window)
        self.setWindowFlags(QtCore.Qt.Window)

    def load_checks(self):
        '''
        Populating the checks with the use of a 'departments.yml' file gives the users the possibility of
        choosing which checks per department they would want in the QC tool.
        Clears all existing check items from the 'checks_layout' layout before populating it with new ones.
        '''
        for index in reversed(range(self.checks_layout.count())):
            widget = self.checks_layout.takeAt(index).widget()
            if widget:
                widget.deleteLater()

        # Getting selected department
        department = self.department_menu.currentText()

        # Creating the department list with 'departments' yaml configuration file (see load_checks DocString for reason)
        with open(QCChecksUI.yml_path, 'r') as stream:
            self.checks = yaml.load(stream, Loader=yaml.FullLoader)

        # Populating checks in dictionary
        self.check_widgets = {}
        for check in self.checks.get(department, []):
            check_widget = QCCheckItemWidget(check)
            self.checks_layout.addWidget(check_widget)
            self.check_widgets[check] = check_widget

    def update_status_color(self, check_name, status):
        """
        Updates the status indicator color for a given check.

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
        '''
        Returning 'checks' dictionary for use in main module
        '''
        return self.checks


if __name__ == '__main__':
    window = QCChecksUI()
    window.show()
