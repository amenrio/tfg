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
from PySide2.QtCore import Qt

HEADER_BUTTON_STYLESHEET = """
        QPushButton {
        text-align: left;
        padding-left: 10px;
        font-size: 13px;
        font-weight: bold;
        background-color: rgb(50,50,50);
        border-radius: 3px;
        }
        QPushButton:hover {
        background-color: rgb(73,73,73)
        }
        QPushButton:pressed {
        background-color: rgb(25, 25, 25);
        }

        """


class CustomToolbox(QWidget):
    """_summary_

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self, department, checker_class_object):
        super().__init__()
        # Name of the toolbox represented by the department to check
        self.department_name = department
        # Instance of the same department checker class
        self.checker_class = checker_class_object

        self.data = self.checker_class.get(self.department_name)

        self.table = QTableWidget(0,0)
        
        self.column_labels = ["Name", "Status"]

        self.header_button = QPushButton(f"▼   {self.department_name.capitalize()}")

        self.vertical_layout = QVBoxLayout()

        self.create_layout()

    def create_layout(self):
        """_summary_
        """
        self.header_button.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Fixed
        )
        self.header_button.setMinimumSize(0, 25)

        self.header_button.setStyleSheet(HEADER_BUTTON_STYLESHEET)

        self.vertical_layout.addWidget(self.header_button)
        self.setLayout(self.vertical_layout)

    def foo(self):

        self.table.setRowCount(len(self.data))

        for row, dpt_step in enumerate(self.data):
            
            condition_checker = self.data.get(dpt_step)
            
            row_item = QTableWidgetItem(condition_checker.displayName)
            row_value = QTableWidgetItem("")
            
            row_item.setToolTip(condition_checker.toolTip)
            row_value.setTextAlignment(Qt.AlignCenter)
            row_value.setToolTip(condition_checker.toolTip)
    
            self.table.setItem(row, 0, row_item)
            self.table.setItem(row, 1, row_value) 
            self.step_index_table.update({dpt_step:row})
            self.set_row_error_level(dpt_step, condition_checker, row_item, row_value)
#        for department_setp, department_condition_checker in self.data.items():
#            self.set_checker_row_error_level(department_setp, department_condition_checker)

    def set_row_error_level(self, dpt_step, condition_checker, row_item, row_value):
        error_level = condition_checker.errorLevel

        bg_color, fg_color, text_color = self.get_error_level_colors(error_level)

        # Movidas de ConditionErrorLevel que no me gustan demasiado

        row_item.setForeground(text_color)
        row_value.setForeground(fg_color)
        row_value.setBackground(bg_color)

        self.update_header_color(dpt_step, error_level)
