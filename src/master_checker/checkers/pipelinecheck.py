import maya.cmds as cmds

import master_checker.common.condition_manager as CM

import master_checker.checkers.basecheck as BaseCheck


import tlc_utils.common.naming as NAMING
from tlc_utils.common import miscutils


class PipelineCheck(BaseCheck.BaseCheck):
    """Pipeline Checker Class

    Args:
        BaseCheck (Class): Base Checker Class
    """

    def __init__(self):
        super().__init__()
        # self.data.clear()
        self.data["pipeline"] = dict()
        self.data["pipeline"]["folder_structure"] = CM.ConditionManager(
            name="folder_structure",
            display_name="Folders structure",
            tooltip="<projID>\00_transDep, 01_dev, 02_prod, 03_post, \
                    maya project in 02_prod, scene structure.",
        )
        self.data["pipeline"]["set_project"] = CM.ConditionManager(
            name="set_project",
            display_name="Maya project",
            tooltip="The project must be inside 02_production.",
        )
        self.data["pipeline"]["scene_structure"] = CM.ConditionManager(
            name="scene_structure",
            display_name="Scene Structure",
            tooltip="Cada escena tiene que seguir la estructura correcta",
        )
        self.data["pipeline"]["namespace"] = CM.ConditionManager(
            name="namespace",
            display_name="Namespace",
            tooltip="There can not be namespace.",
        )
        self.data["pipeline"]["user"] = CM.ConditionManager(
            name="user",
            display_name="User",
            tooltip="1º field three capital letters, ex.: ABC_",
        )
        self.data["pipeline"]["multiple_shapes"] = CM.ConditionManager(
            name="multiple_shapes",
            display_name="Multiple shapes",
            tooltip="No transform node can contain multiple shape nodes.",
        )
        self.data["pipeline"]["zero_local_values"] = CM.ConditionManager(
            name="zero_local_values",
            display_name="Zero local values",
            tooltip="No transform node can have non-zero values in local space.",
        )
        self.data["pipeline"]["references"] = CM.ConditionManager(
            name="references", display_name="References", tooltip="Missing references."
        )
        self.data["pipeline"]["instanced_nodes"] = CM.ConditionManager(
            name="instanced_nodes", display_name="Instanced nodes", tooltip="IDK."
        )
        self.data["pipeline"]["inside_groups"] = CM.ConditionManager(
            name="inside_groups",
            display_name="Inside groups",
            tooltip="All elements of the scene must be within groups.",
        )
        self.data["pipeline"]["locked_groups"] = CM.ConditionManager(
            name="locked_groups",
            display_name="Locked groups",
            tooltip="All groups must be blocked.",
        )
        self.data["pipeline"]["blendshapes"] = CM.ConditionManager(
            name="blendshapes",
            display_name="Blendshapes",
            tooltip="There cannot be blendshapes",
        )
        self.data["pipeline"]["scales"] = CM.ConditionManager(
            name="scales",
            display_name="Scales",
            property_flag=CM.ConditionManager.PROPERTY_FIXABLE
            + CM.ConditionManager.PROPERTY_IGNORABLE,
            tooltip="Scales = 1",
        )
        self.data["pipeline"]["animation_keys"] = CM.ConditionManager(
            name="animation_keys",
            display_name="Animation keys",
            tooltip="No animatable objets with keys",
        )
        self.data["pipeline"]["unknown_nodes"] = CM.ConditionManager(
            name="unknown_nodes",
            display_name="Unknown nodes",
            tooltip="There cannot be unknown nodes, \
                uncheck Outline/Display/DAG objects only to see them.",
        )
        self.data["pipeline"]["empty_nodes"] = CM.ConditionManager(
            name="empty_nodes",
            display_name="Empty Nodes",
            tooltip="There cannot be empty nodes.",
        )

    def check_empty_nodes(self):
        """_summary_"""
        error_list = miscutils.getEmptyGroups()
        self.data["pipeline"]["empty_nodes"].set_elements(error_list)
        self.data["pipeline"]["empty_nodes"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def check_set_project(self):
        """Checks that the last folder of the current setted workspace is pipeline compliant
        sets error if las folder is different from pipeline naming guide
        """
        # Get current workspace root folder
        current_workspace = cmds.workspace(q=True, rd=True)
        # Splits workspace path and gets last folder name
        last_folder_in_workspace_path = current_workspace.split("/")[:-1][-1]
        # Compares last folder name with pipeline naming guide
        if last_folder_in_workspace_path != NAMING.topDirs.get("PRE+PROD"):
            self.data["pipeline"]["set_project"].count = 1
        self.data["pipeline"]["set_project"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def check_namespace(self):
        """Checks the scene namespaces (minus defaut ones), sets error level if not zero"""
        # Returns namespace list
        namespace_list = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
        # Removes default values
        namespace_list.remove("UI")
        namespace_list.remove("shared")

        # Set elements based on list
        self.data["pipeline"]["namespace"].set_elements(namespace_list)
        # Error level is given when namespace list is not empty
        self.data["pipeline"]["namespace"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def check_scales(self):
        """Checks every node scale and sets error level if the scale is not (1, 1, 1)"""
        error_objects = []

        for obj in self.objects_list:
            try:
                object_scale = cmds.getAttr(f"{obj}.scale")
                if object_scale != [(1.0, 1.0, 1.0)]:
                    error_objects.append(obj)
            except Exception:
                print(f"Obj {obj} does not have scale")
                continue

        # Obtener el count en otro lado ¿?
        #  podria tenerse la lista de objetos en el data directamente,
        # si queremos la longitud podriamos utilizar el metodo len despues
        self.data["pipeline"]["scales"].set_elements(error_objects)
        self.data["pipeline"]["scales"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def fix_scales(self, error_objects):
        """Fix function for scale checklist
        Sets transform node scale to 1
        DANGEROUS, ONLY TESTING PURPOSE

        Args:
            error_objects (list): List of objects setted as errors.
        """
        for o in error_objects:
            cmds.setAttr((o + ".scaleX"), 1)
            cmds.setAttr((o + ".scaleY"), 1)
            cmds.setAttr((o + ".scaleZ"), 1)

    def check_folder_structure(self):
        """TODO
        """

    def check_user(self):
        """TODO
        """

    def check_multiple_shapes(self):
        """TODO
        """

    def check_zero_local_values(self):
        """TODO
        """

    def check_references(self):
        """TODO
        """

    def check_instanced_nodes(self):
        """TODO
        """

    def check_inside_groups(self):
        """TODO
        """

    def check_blocked_groups(self):
        """TODO
        """

    def check_blendshapes(self):
        """TODO
        """

    def check_animation_keys(self):
        """TODO
        """

    def check_unknown_nodes(self):
        """TODO
        """
