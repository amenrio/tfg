import maya.cmds as cmds

import master_checker.checkers.basecheck as BaseCheck
import master_checker.common.condition_manager as CM

import tlc_utils.common.naming as NAMING


class NamingCheck(BaseCheck.BaseCheck):
    """Naming Check Class

    Args:
        BaseCheck (class): Abstract checker class
    """

    def __init__(self):
        super().__init__()
        # self.data.clear()
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
        """Check function
        Searches for PIPE '|' character in node names, if found, adds item to error list
        Error level is setted if error list is not 0
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
        """Helper Function

        Args:
            node (str): Node name

        Returns:
            bool: Returns if node is group of other transforms and doesnt have shapes as children
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
        """Checker function
        Chekcs for every node if its a group with a helper function (is_group)
        Then checks if groupId part of name is pipeline compliant
        Sets error level if list_errors is not 0
        """
        error_list = list()
        for obj in self.objects_list:
            if self.is_group(obj):
                obj_name_parts = self.get_nice_name(obj)
                if not isinstance(obj_name_parts, list):
                    error_list.append(obj)
                if obj_name_parts[0] not in NAMING.naming_maya.get("group"):
                    error_list.append(obj)
        self.data["naming"]["groups_id"].set_elements(error_list)
        self.data["naming"]["groups_id"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def check_nodes_id(self):
        """Chekcer function
        Checks for every node if nodes_id mathces naming pipeline rules
        Sets error level if error_list is not 0
        """
        error_list = list()
        for obj in self.objects_list:
            obj_name_parts = self.get_nice_name(obj)
            if not isinstance(obj_name_parts, list):
                error_list.append(obj)
            if obj_name_parts[0] not in NAMING.naming_maya.values():
                error_list.append(obj)

        self.data["naming"]["nodes_id"].set_elements(error_list)
        self.data["naming"]["nodes_id"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def check_position_field(self):
        """Checker function
        Checks for every node if its position_field matches naming pipeline rules
        Sets error level if error_list is not 0
        """
        error_list = list()
        for obj in self.objects_list:
            obj_name_parts = self.get_nice_name(obj)
            if not isinstance(obj_name_parts, list):
                error_list.append(obj)
            if obj_name_parts[1] not in NAMING.location_flags.values():
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
        """Checker function
        Checks for every node if its node Fields are 3
        Sets error level if error_list is not 0

        Returns:
            list: Error objects
        """
        error_objects = []

        for obj in self.objects_list:
            obj_nice_name = self.get_nice_name(obj)
            if len(obj_nice_name) != 3:
                error_objects.append(obj)

        self.data["naming"]["node_fields"].set_elements(error_objects)
        # self.data["naming"]["node_fields"].set_error_level(
        #          CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO)
        # return error_objects

    def get_nice_name(self, name_obj):
        """Helper function

        Args:
            name_obj (str): Node Name

        Returns:
            list: List of node_fields
        """
        if name_obj.find("_") == -1:
            return name_obj
        if name_obj.find(":") != -1:
            return self.get_nice_name(name_obj.split(":")[-1])
        if name_obj.find("|") != -1:
            return self.get_nice_name(name_obj.split("|")[-1])
        output = name_obj.split("_")
        return output

    def fix_node_fields(self, error_objects):
        """Fix function
        not implemented yet

        Args:
            error_objects (list): error_objects
        """
        for o in error_objects:
            if len(o.split("_")) == 2:
                cmds.rename(o, o + "_")
            elif len(o.split("_")) == 1:
                cmds.rename(o, "_" + o + "_")

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
