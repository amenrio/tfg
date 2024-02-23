#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by: Andres Mendez <amenrio@gmail.com>

"""Naming Checker Class

This module defines the naming checker class that inherits from the BaseCheck class.
It contains the methods to run the checks defined in the data dictionary.
"""

import maya.cmds as cmds

import master_checker.checkers.basecheck as BaseCheck
import master_checker.common.condition_manager as CM

import tlc_utils.common.naming as NAMING


class NamingCheck(BaseCheck.BaseCheck):
    """Naming Check Class
    
    This class is the naming checker class. It contains the methods destined to compare the scene's
    objects names with the naming pipeline rules.
    
    Args:
        BaseCheck (class): Abstract checker class
    Attributes:
        data (dict): Dictionary that holds each department checker and their respective methods
        objects_list (list): List of objects to run the checks on
    """

    def __init__(self):
        """Naming Checker Class Constructor
        
        Initializes the data dictionary, adds the naming department to it and initializes naming 
        methods and condition managers.
        """
        super().__init__()

        self.data["naming"] = {}
        self.data["naming"]["scene_name"] = CM.ConditionManager(
            name="scene_name",
            display_name="Scene Name",
            tooltip="Correct naming of the scene, \
                <projID>_<typeID>_<deptmD>_<assetID>_<version>_<workingVersion>",
        )
        self.data["naming"]["node_fields"] = CM.ConditionManager(
            name="node_fields",
            display_name="Node fields",
            property_flag=CM.ConditionManager.PROPERTY_SELECTABLE
            + CM.ConditionManager.PROPERTY_FIXABLE
            + CM.ConditionManager.PROPERTY_IGNORABLE,
            tooltip="Every node name in the scene with three fields but lights.",
        )
        self.data["naming"]["nodes_id"] = CM.ConditionManager(
            name="nodes_id",
            display_name="Node ID",
            tooltip="1º field must correctly identify the type of node.",
        )
        self.data["naming"]["groups_id"] = CM.ConditionManager(
            name="groups_id", display_name="Groups ID", tooltip="Groups 1º field -> grp"
        )
        self.data["naming"]["locators_id"] = CM.ConditionManager(
            name="locators_id",
            display_name="Locators ID",
            tooltip="Locators 1º field -> lct",
        )
        self.data["naming"]["splines_id"] = CM.ConditionManager(
            name="splines_id",
            display_name="Splines ID",
            tooltip="Splines 1º field -> spl",
        )
        self.data["naming"]["cameras_id"] = CM.ConditionManager(
            name="cameras_id",
            display_name="Cameras ID",
            tooltip="Cameras 1º field -> cam",
        )
        self.data["naming"]["position_field"] = CM.ConditionManager(
            name="position_field",
            property_flag=CM.ConditionManager.PROPERTY_SELECTABLE
            + CM.ConditionManager.PROPERTY_FIXABLE
            + CM.ConditionManager.PROPERTY_IGNORABLE,
            display_name="Position field",
            tooltip="2ª field must identify the node correct position in the scene \
                    _x_/_l_/_r_/_c_.",
        )
        self.data["naming"]["node_name"] = CM.ConditionManager(
            name="node_name",
            display_name="Node name",
            tooltip="3º field must correctly identify the name of the node.",
        )
        self.data["naming"]["input_connections"] = CM.ConditionManager(
            name="input_connections",
            display_name="Input connections",
            tooltip="Imput connections name with three fields.",
        )
        self.data["naming"]["transforms_shapes"] = CM.ConditionManager(
            name="transforms_shapes",
            display_name="Transforms shapes",
            tooltip="Shape name = Transform name + shape.",
        )
        self.data["naming"]["invalid_characters"] = CM.ConditionManager(
            name="invalid_characters",
            display_name="Invalid characters",
            tooltip="Non invalid characters or spaces.",
        )

        self.data["naming"]["unique_names"] = CM.ConditionManager(
            name="unique_names",
            display_name="Duplicate Nodes",
            tooltip="Nodes can't be duplicated",
        )

        self.data["naming"]["lights_naming"] = CM.ConditionManager(
            name="lights_naming",
            display_name="Lights naming",
            tooltip="Every light in the scene with four fields.",
        )
        self.data["naming"]["layers_naming"] = CM.ConditionManager(
            name="layers_naming",
            display_name="Layers naming",
            tooltip="Display and animation layers naming divided in two fields-> ly_<layerID>",
        )
        self.data["naming"]["groups_layers_id"] = CM.ConditionManager(
            name="groups_layers_id",
            display_name="Groups layers ID",
            tooltip="Group layersID: grp_x_geo -> geo/grp_x_rig -> rig/...light/...anim/...puppet",
        )

    def check_unique_names(self):
        """Method to check for non unique names in the scene
        
        Searches for PIPE '|' character in node names, if found, adds item to error list
        Sets the check's condition manager error level if error list is not 0
        """
        error_list = list()
        for obj in self.objects_list:
            if obj.find("|") > 0:
                error_list.append(obj)
        self.data["naming"]["unique_names"].set_elements(error_list)
        self.data["naming"]["unique_names"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def is_group(self, node):
        """Auxiliary method to check if a node is a group
        Args:
            node (str): Node name
        Returns:
            bool: True if node is a group, False otherwise
        """
        if not cmds.objectType(node, isType="transform"):
            return False
        try:
            children = cmds.listRelatives(node, c=True)
            for child in children:
                if not cmds.ls(child, transforms=True):
                    return False
                return True
        except Exception:
            return False

    def check_groups_id(self):
        """Method to check for correct group naming

        Using the is_group method, checks every node in the scene to see if it's a group.
        The object's name is then split into tokens. 
        If the get_name_tokens doesn't return a list, the object is added to the error list.
        If the first token is not pipeline compliant, the object is added to the error list.
        The check's condition manager error level is set to True if the error list is not 0
        """

        error_list = list()
        for obj in self.objects_list:
            if self.is_group(obj):
                obj_name_tokens = self.get_name_tokens(obj)
                if not isinstance(obj_name_tokens, list):
                    error_list.append(obj)
                if obj_name_tokens[0] not in NAMING.naming_maya.get("group"):
                    error_list.append(obj)
        self.data["naming"]["groups_id"].set_elements(error_list)
        self.data["naming"]["groups_id"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def check_nodes_id(self):
        """Method to check id token for every node in the scene

        If the get_name_tokens doesn't return a list, the object is added to the error list.
        If the first token is not pipeline compliant, the object is added to the error list.
        The check's condition manager error level is set to True if the error list is not 0
        
        TODO: Add methods to check each node-type rules (geometry, locators, splines, cameras, etc)
        """
        error_list = list()
        for obj in self.objects_list:
            obj_name_tokens = self.get_name_tokens(obj)
            if not isinstance(obj_name_tokens, list):
                error_list.append(obj)
            if obj_name_tokens[0] not in NAMING.naming_maya.values():
                error_list.append(obj)

        self.data["naming"]["nodes_id"].set_elements(error_list)
        self.data["naming"]["nodes_id"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def check_position_field(self):
        """Method to check the position field token for every node in the scene

        If the get_name_tokens doesn't return a list, the object is added to the error list.
        If the second token is not pipeline compliant, the object is added to the error list.
        The check's condition manager error level is set to True if the error list is not 0
        """
        error_list = list()
        for obj in self.objects_list:
            obj_name_tokens = self.get_name_tokens(obj)
            if not isinstance(obj_name_tokens, list):
                error_list.append(obj)
            if obj_name_tokens[1] not in NAMING.location_flags.values():
                error_list.append(obj)

        self.data["naming"]["position_field"].set_elements(error_list)
        self.data["naming"]["position_field"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )
        # pprint(self.data["naming"]["position_field"].get_elements())

    def fix_position_field(self, error_elements):
        """TODO
        """
        # error_elements = self.data["naming"]["position_field"].get_elements()
        print(error_elements)

    def check_node_fields(self):
        """Method to check if every node's name has only 3 tokens

        If the get_name_tokens doesn't return a list with 3 elements, the object is added to
        the error list.
        The check's condition manager error level is set to True if the error list is not 0
        """
        error_objects = []

        for obj in self.objects_list:
            obj_nice_name = self.get_name_tokens(obj)
            if len(obj_nice_name) != 3:
                error_objects.append(obj)

        self.data["naming"]["node_fields"].set_elements(error_objects)
        # self.data["naming"]["node_fields"].set_error_level(
        #          CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO)
        # return error_objects

    def get_name_tokens(self, name_obj):
        """Recursive method to get the tokens from a node name

        Using the find method, checks for these characters in the node name ['_', ':', '|'].
        If it doesn't find a '_', returns the name_obj.
        If it finds a ':' (Namespace), it calls itself with the last token, ignoring the namespace and
        returns the resulting operation.
        If it finds a '|', it calls itself with the last token, ignoring the parent, and returns the
        resulting operation.
        If those conditions are not met, it splits the name_obj using the '_' character and returns
        the resulting list.

        Args:
            name_obj (str): Node name

        Returns:
            tokens (list): List of tokens

        TODO: Differentiate between namespace and parent errors
        """
        if name_obj.find("_") == -1:
            return name_obj
        if name_obj.find(":") != -1:
            return self.get_name_tokens(name_obj.split(":")[-1])
        if name_obj.find("|") != -1:
            return self.get_name_tokens(name_obj.split("|")[-1])
        tokens = name_obj.split("_")
        return tokens 

    def fix_node_fields(self):
        """TODO
        """
    # def checkFoldersStructure(self):

    # def fixFoldersStructure(self):

    def check_scene_name(self):
        """TODO
        """

    def check_locators_id(self):
        """TODO
        """

    def check_splines_id(self):
        """TODO
        """

    def check_cameras_id(self):
        """TODO
        """

    def check_node_name(self):
        """TODO
        """

    def check_input_connections(self):
        """TODO
        """

    def check_transforms_shapes(self):
        """TODO
        """

    def check_invalid_characters(self):
        """TODO
        """

    def check_lights_naming(self):
        """TODO
        """

    def check_layers_naming(self):
        """TODO
        """

    def check_groups_layers_id(self):
        """TODO
        """

    def check_rigging_test(self):
        """TODO
        """
