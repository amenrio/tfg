"""_summary_

Returns:
    _type_: _description_
"""
import importlib
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QTableWidgetItem,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QTableWidget,
    QMenu,
    QAction,
    QSizePolicy,
    QAbstractScrollArea,
    QAbstractItemView,
)
from PySide2.QtGui import QBrush, QColor, QGradient, QGuiApplication, QPalette
import PySide2.QtWidgets as QtWidgets

import master_checker.master_checker as main

import master_checker.checkers.namingcheck as Naming
import master_checker.checkers.pipelinecheck as Pipeline
import master_checker.checkers.riggingcheck as Rigging
import master_checker.checkers.basecheck as BaseCheck

import master_checker.common.custom_toolbox as CustomToolbox

import tlc_utils.common.qtutils as qtutils

importlib.reload(CustomToolbox)
importlib.reload(main)
importlib.reload(Naming)
importlib.reload(Pipeline)
importlib.reload(Rigging)
importlib.reload(BaseCheck)


class MasterCheckerUI(qtutils.CheckerWindow):
    """UI Class for master of checkers code.

    Args:
        qtutils (_type_): _description_
    """

    def __init__(self, department="DEFAULT", parent=qtutils.getMayaMainWindow()):
        ui_file = f"{os.path.splitext(os.path.basename(__file__))[0]}.ui"
        title = "Master of Checkers"
        print(ui_file)
        super(MasterCheckerUI, self).__init__(
            f"{os.path.dirname(__file__)}/ui/{ui_file}", title, parent
        )
        self.main = main.MasterChecker(department)
        self.main.run_all()
        self.department_toolbox_dict = {}
        self.__init_ui__()
        self.show()

    def __init_ui__(self):
        for department in self.main.departments_checker_data.keys():
            department_toolbox = self._init_step_toolbox(department)
            self._init_toolbox_rows(department_toolbox)

    def _init_step_toolbox(self, department):
        department_checker_class = self.main.departments_checker_classes.get(department)
        department_toolbox = CustomToolbox.CustomToolbox(
            department, department_checker_class
        )
        self.department_toolbox_dict.update({department: department_toolbox})

        return department_toolbox

    def _init_toolbox_rows(self, department_toolbox):
        """Sets the rows of the toolbox object based on that department checklist

        Args:
            department_toolbox (CustomToolbox): Department's custom toolbox object
            department (str): Department's Name
        """
        # self.ui.departmentsVL.addWidget(department_toolbox)
        self.ui.verticalLayout_01.addWidget(department_toolbox)

        # self.ui.departmentsVL.addWidget(department_toolbox)
