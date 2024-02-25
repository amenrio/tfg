#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by: Andres Mendez <amenrio@gmail.com>

"""Rigging Checker Module

This module defines the rigging checker class. This class is a specialized checker class that inherits
from the NamingCheck and PipelineCheck classes. It contains all the methods and condition managers for
the rigging department.
"""

import maya.cmds as cmds

import master_checker.common.condition_manager as CM

from master_checker.checkers.namingcheck import NamingCheck
from master_checker.checkers.pipelinecheck import PipelineCheck


class RiggingCheck(NamingCheck, PipelineCheck):
    """Rigging Checker Class

    This class contains all the methods and condition managers for the rigging department.
    It inherits from the NamingCheck and PipelineCheck classes so it also runs all the checks
    from those.

    Args:
        NamingCheck (Class): Naming Checker Class
        PipelineCheck (Class): Pipeline Checker Class
    Attributes:
        data (dict): Dictionary that holds each department checker and their respective methods
        objects_list (list): List of objects to run the checks on
    """

    def __init__(self):
        """Rigging Checker Class Constructor
        
        Initializes both the NamingCheck and PipelineCheck classes.
        Initializes the data dictionary, adds the rigging department's methods and condition managers
        """

        super().__init__()
        # super(RiggingCheck).__init__(NamingCheck)
        # super(RiggingCheck).__init__(PipelineCheck)

        self.data["rigging"] = dict()
        # self.data.update({"rigging":{}})
        self.data["naming"]["joint_naming"] = CM.ConditionManager(
                name="joint_naming", display_name="Joint Naming", tooltip="Joint Naming"
            )
        self.data["rigging"]["rigging_test"] = CM.ConditionManager(
                name="rigging_test", display_name="rigging_test", tooltip="Rig Test"
            )
