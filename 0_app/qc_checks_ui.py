
# Quality Control Checks UI *********************************************************************
# 
# This is the UI for the Quality Control Checks, performed by department users.
# It gives the user the ability to see a report based on checks that fails, select
# the checks they want to resolve automatically with a "Fix This" button, run a selected check
# again, and "Publish" when all is "passed".
#
# date    = 2024-08-30
# author  = Stephane Barbin
#*********************************************************************************************


# QUALITY CONTROL CHECKS UI (qc)
# ____________________________________________________________________________________________


# IMPORTING MODULES
from PySide2 import QtWidgets, QtCore, QtGui


# ____________________________________________________________________________________________



def qc_checks_ui():

    # FUNCTIONS
    # Select All
    def select_all():
        for qc_list in range(qc_list_widget.count()):
            list_item = qc_list_widget.item(qc_list)
            list_item.setSelected(True)

    # Select None
    def select_none():
        qc_list_widget.clearSelection()

    # Invert Selection
    def invert_selection():
        for qc_list in range(qc_list_widget.count()):
            list_item = qc_list_widget.item(qc_list)
            list_item.setSelected(not list_item.isSelected())

    # Department choice
    def department_selection():
        qc_list_widget.clear()
        selected_department = department_menu.currentText()
        
        if selected_department == 'Modeling':
            qc_list_widget.addItems([
                                    "Animated Objects",
                                    "Scene Cleanup",
                                    "Center",
                                    "Freeze Transform"
                                    ])
            qc_list_widget.sortItems()
        elif selected_department == 'Rigging':
            qc_list_widget.addItems([
                                    "Animated Objects",
                                    "Layer Organization",
                                    "Scene Cleanup",
                                    "Joints Influence Count",
                                    "Control Shape Consistency",
                                    "Joints Naming",
                                    "Controllers Naming"
                                    ])
            qc_list_widget.sortItems()
        elif selected_department == 'Animation':
            qc_list_widget.addItems([
                                    "Keyframe Analysis",
                                    "In-Betweens",
                                    "Rigging Checks",
                                    "Redundant Keyframes",
                                    "Scene Cleanup",
                                    "Layer Organization"
                                    ])
            qc_list_widget.sortItems()


    # Create a QWidget for the main window
    qc_window = QtWidgets.QWidget()


    # Set window title and size
    qc_window.setWindowTitle("Quality Control Checks")
    qc_window.setGeometry(600, 200, 500, 700)


    # Create the main layout
    main_layout = QtWidgets.QVBoxLayout(qc_window)


    # Department dropdown menu
    department_menu = QtWidgets.QComboBox()
    department_menu.addItems(["Modeling", "Rigging", "Animation"])
    main_layout.addWidget(department_menu)


    # Qality Control Checks list title
    qc_title = QtWidgets.QLabel("Quality Control Check List")
    qc_title.setAlignment(QtCore.Qt.AlignCenter)
    qc_title.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
    main_layout.addWidget(qc_title)


    # List of Quality Control Checks per department
    qc_list_widget = QtWidgets.QListWidget()
    qc_list_widget.addItems([
                            "Animated Objects",
                            "Scene Cleanup",
                            "Center",
                            "Freeze Transform"
                            ])
    qc_list_widget.sortItems()
    qc_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    main_layout.addWidget(qc_list_widget)


    # Buttons "Select All", "Select None", "Invert Selection"
    select_btn_layout = QtWidgets.QHBoxLayout()
    select_all_btn = QtWidgets.QPushButton("Select All")
    select_none_btn = QtWidgets.QPushButton("Select None")
    invert_selection_btn = QtWidgets.QPushButton("Invert Selection")
    select_btn_layout.addWidget(select_all_btn)
    select_btn_layout.addWidget(select_none_btn)
    select_btn_layout.addWidget(invert_selection_btn)
    main_layout.addLayout(select_btn_layout)


    # Button "Run Selected"
    run_selected_btn = QtWidgets.QPushButton("Run Selected")
    main_layout.addWidget(run_selected_btn)


    # Button "Fix This"
    fix_this_btn = QtWidgets.QPushButton("Fix This")
    main_layout.addWidget(fix_this_btn)


    # Status labels with background colors
    status_layout = QtWidgets.QHBoxLayout()
    passed_label = QtWidgets.QLabel("Passed: 0")
    passed_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
    status_layout.addWidget(passed_label)
    warning_label = QtWidgets.QLabel("Warning: 0")
    warning_label.setStyleSheet("background-color: yellow; color: black; padding: 5px;")
    status_layout.addWidget(warning_label)
    failed_label = QtWidgets.QLabel("Failed: 0")
    failed_label.setStyleSheet("background-color: red; color: white; padding: 5px;")
    status_layout.addWidget(failed_label)
    main_layout.addLayout(status_layout)


    # Window for checks report
    results_window = QtWidgets.QTextEdit()
    results_window.setReadOnly(True)
    main_layout.addWidget(results_window)

    # Button "Publish"
    publish_btn = QtWidgets.QPushButton("Publish")
    main_layout.addWidget(publish_btn)


    # Button connection to functions
    select_all_btn.clicked.connect(select_all)
    select_none_btn.clicked.connect(select_none)
    invert_selection_btn.clicked.connect(invert_selection)
    department_menu.currentIndexChanged.connect(department_selection)

    return (qc_window, fix_this_btn, department_menu, qc_list_widget, 
            run_selected_btn, passed_label, warning_label, failed_label, results_window,
            select_all_btn, select_none_btn, invert_selection_btn, publish_btn)

