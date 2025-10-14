from lerobot.src.lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.src.lerobot.record import record_loop
from lerobot.src.lerobot.policies.act.modeling_act import ACTPolicy
from lerobot.src.lerobot.robots.robot import Robot
from lerobot.src.lerobot.teleoperators.teleoperator import Teleoperator


def load_policy(policy_name: str) -> ACTPolicy:
    return ACTPolicy.from_pretrained(policy_name)


def load_multiple_policies(policies_name: list[str]) -> list[ACTPolicy]:
    return [load_policy(policy_name) for policy_name in policies_name]


def execute_multiple_policies(
    policies_name: list[str],
    robot: Robot,
    events: dict,
    fps: int,
    dataset: LeRobotDataset | None = None,
    teleop: Teleoperator | list[Teleoperator] | None = None,
    control_time_s: int | None = None,
    single_task: str | None = None,
    display_data: bool = False,
):
    policies = load_multiple_policies(policies_name)
    for policy in policies:
        record_loop(
            robot,
            events,
            fps,
            dataset,
            teleop,
            policy,
            control_time_s,
            single_task,
            display_data,
        )
