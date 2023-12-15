import maya.cmds as cmds

import master_checker.common.condition_manager as CM

from master_checker.checkers.namingcheck import NamingCheck
from master_checker.checkers.pipelinecheck import PipelineCheck


class RiggingCheck(NamingCheck, PipelineCheck):
    """_summary_

    Args:
        NamingCheck (_type_): _description_
        PipelineCheck (_type_): _description_
    """

    def __init__(self):
        super().__init__()
        # super(RiggingCheck).__init__(NamingCheck)
        # super(RiggingCheck).__init__(PipelineCheck)

        self.data["rigging"] = dict()
        # self.data.update({"rigging":{}})
        self.data["naming"]["joint_naming"] = {
            CM.ConditionManager(
                name="joint_naming", display_name="Joint Naming", tooltip="Joint Naming"
            )
        }
        self.data["rigging"]["rigging_test"] = {
            CM.ConditionManager(
                name="rigging_test", display_name="rigging_test", tooltip="Rig Test"
            )
        }

    def check_joint_naming(self):
        """_summary_
        """
        self.data["naming"]["joint_naming"].set_elements([1])
        self.data["naming"]["joint_naming"].set_error_level(
            CM.ConditionErrorCriteria.ERROR_WHEN_NOT_ZERO
        )

    def check_rigging_test(self):
        print("Jeje")
