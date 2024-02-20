#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by: Andres Mendez <amenrio@gmail.com>

"""Base Checker Class

This module defines the base checker class that each deparmtnet's checker class will inherit from.
Aditionally, using python's builtin 'getattr' function, it allows for dynamic method calling. Avoiding
the need to call each department's method individually.

Example:
    To create a new checker class, you can inherit from BaseCheck and add your own 'check' and 
    'fix' methods to it.

    class MyDepartmentChecker(BaseCheck):
        def __init__(self):
            super().__init__()
            # Add your check methods and condition managers to the data's department dictionary
            pass

        def check_my_check(self):
            # Your check logic here
            pass

        def fix_my_check(self, error_list):
            # Your fix logic here
            pass
"""

class BaseCheck():
    """Base Checker Class

    This class is the base class for all department checker classes. It contains the basic structure
    and methods that each department's checker class will inherit from.

    Attributes:
        data (dict): Dictionary that holds each department checker and their respective methods
        objects_list (list): List of objects to run the checks on

    """

    def __init__(self):
        """Base Checker Class Constructor

        Initializes the data dictionary and the objects_list list
        """
        self.data: dict = dict()
        self.objects_list: list = list()

    def update_object_list(self, scene_objects):
        """Update the list of objects to run the checks on

        Args:
            scene_objects (list): List of objects to run the checks on
        """
        self.objects_list = scene_objects

    def check_all(self, public_nodes):
        """Abstract method to run all checks defined in the data dictionary

        Using python's builtin 'getattr' function, this method allows for dynamic method calling.
        Formating the method name to call using the 'check_' prefix and the function name as the suffix.
        If the method is not implemented, it will print a message and skip it.

        Args:
            public_nodes (list): List of public nodes to run the checks on
        """
        self.objects_list = public_nodes

        functions = []
        for checker_dict in self.data.values():
            functions.extend(checker_dict.keys())

        for func in functions:
            try:
                check = getattr(self, f"check_{func}")
                check()
            except AttributeError:
                print(f"Method {func} not implemented yet, skipping...")
                continue

    def check_func(self, public_nodes, _func):
        """Run specific department's check method

        Using python's builtin 'getattr' function, this method allows for dynamic method calling.
        Formating the method name to call using the 'check_' prefix and the function name as the suffix.
        If the method is not implemented, it will print a message and skip it.

        Args:
            public_nodes (list): List of public nodes to run the check on
            _func (string): basname of the function to run
        """
        self.objects_list = public_nodes
        try:
            check = getattr(self, f"check_{_func}")
            check()
        except AttributeError:
            print(f"Method to Check {_func} {self} not implemented yet, skipping...")
            return

    def fix_func(self, error_list, _func):
        """Run specific department's fix method

        Using python's builtin 'getattr' function, this method allows for dynamic method calling.
        Formating the method name to call using the 'fix_' prefix and the function name as the suffix.
        If the method is not implemented, it will print a message and skip it.

        Args:
            error_list (list): List of public nodes that fail the check
            _func (string): basname of the function to run
        """
        try:
            check = getattr(self, f"fix_{_func}")
            check(error_list)
        except AttributeError:
            print(f"Method to Fix {_func} not implemented yet, skipping...")
            return
