import os
import sys

# import importlib
# DEPARTMENT_CHECK_IMPORT_PATH = 'master_checker.departments.{department}'

import master_checker.checkers.basecheck as Base
import master_checker.checkers.pipelinecheck as Pipeline
import master_checker.checkers.namingcheck as Naming
import master_checker.checkers.riggingcheck as Rigging

import tlc_utils.common.pipeline as pipeline_utils
import tlc_utils.common.miscutils as misc_utils


class MasterChecker:
    """The MasterChecker class holds the main logic for running all the checks necessary
    for the current production department. It also holds the data for all the checks ran.
    
    Attributes:
        scene_objects (list): List of all nodes that need to pass all the pipeline checks
        departments_to_run (list): List of department checkers to run based on current production department
        departments_checker_classes (dict): Dictionary for department checker classes:
            {"department_name": department_checker_class}
        departments_checker_data (dict): Dictionary for department checker data:
            {'department_name': {department_check_function: ConditionChecker Class}}
    TODO:
        TODO TODO  :)
    """

    def __init__(self, dpt_id="DEFAULT"):
        # List of all nodes that need to pass all the pipeline checks
        self.scene_objects = []
        # Gets list of department checkers to run based on current production department
        self.departments_to_run = ["pipeline","naming"]
        self.departments_to_run.extend(pipeline_utils.checkers_from_dptID.get(dpt_id))
        # Dictionary for department checker classes:
        # {"department_name": department_checker_class}
        self.departments_checker_classes = dict()
        # Dictionary for department checker data:
        # {'department_name': {department_check_function: ConditionChecker Class}}
        self.departments_checker_data = dict()

        self.get_department_checker_classes()

    def get_department_checker_classes(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        for department in self.departments_to_run:
            department_checker_class = self.get_department_class_instance(department)
            self.departments_checker_classes.update(
                {department: department_checker_class()}
            )
        return self.departments_checker_classes

    def get_department_class_instance(self, department):
        """_summary_

        Args:
            department (_type_): _description_

        Returns:
            _type_: _description_
        """
        # department_import_cmd = DEPARTMENT_CHECK_IMPORT_PATH.format(department)
        departmet_module = globals()[department.capitalize()]
        department_checker_class = getattr(
            departmet_module, f"{department.capitalize()}Check"
        )

        return department_checker_class

    def run_all(self):
        """_summary_
        """
        self.scene_objects = misc_utils.get_public_nodes()
        for checker_class in self.departments_checker_classes.values():
            checker_class.check_all(self.scene_objects)
            self.departments_checker_data.update(checker_class.data)

    def run_check(self, department):
        """_summary_

        Args:
            department (_type_): _description_
        """
        misc_utils.get_public_nodes()
        department_checker_class = self.departments_checker_classes.get(department)
        department_checker_class().check_all(self.scene_objects)
