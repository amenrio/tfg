"""_summary_
"""
from PySide2.QtWidgets import QMenu, QAction


class Menu(QMenu):
    """_summary_

    Args:
        QMenu (_type_): _description_
    """

    def __init__(self, page, item_row, toolbox, checker_class, department_step):
        super().__init__()

        self.page = page
        self.item_row = item_row
        self.toolbox = toolbox
        self.checker_class = checker_class
        self.department_step = department_step
        self.action_recheck = QAction("Recheck")
        self.action_select = QAction("Select")
        self.action_ignore = QAction("Ignore")
        self.action_fix = QAction("Fix")

    def add_recheck(self):
        """_summary_
        """
        self.action_recheck.triggered.connect(
            lambda: self.toolbox.run_row_checker(
                self.checker_class, self.department_step
            )
        )
        self.insertAction(None, self.action_recheck)

    def add_select(self):
        """_summary_
        """
        self.action_select.triggered.connect(
            lambda: self.toolbox.select_error_nodes(
                self.checker_class, self.department_step
            )
        )
        self.insertAction(None, self.action_select)

    def add_ignore(self):
        """_summary_
        """
        self.action_ignore.triggered.connect(
            lambda: self.toolbox.ignore_condition_checker(
                self.checker_class, self.department_step
            )
        )
        self.insertAction(None, self.action_ignore)

    def add_fix(self):
        """_summary_
        """
        self.action_fix.triggered.connect(
            lambda: self.toolbox.run_fix_checker(
                self.checker_class, self.department_step
            )
        )
        self.insertAction(None, self.action_fix)
