"""This module Holds the base class which every other checker inherits from
"""

class BaseCheck():
    """Abstract Checker Function
    Holds every common methods
    """

    def __init__(self):
        self.data: dict = dict()
        self.objects_list: list = list()

    def update_object_list(self, scene_objects):
        """Updates self.object list to most recent execution

        Args:
            scene_objects (list): scene object list
        """
        self.objects_list = scene_objects

    def check_all(self, public_nodes, _func=None):
        """
        Abstract function that runs every checker function listed in the 'data' dictionary.

        _extended_summary_

        :param public_nodes: List of nodes present in the scene to check
        :type public_nodes: list
        :param _func: If _func parameter is given, it will only run that check function, defaults to None
        :type _func: _type_, str
        """
        self.objects_list = public_nodes

        functions = _func

        if not _func:
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
        """ Run specific function's check method

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
        """Run specific function's fix method

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
