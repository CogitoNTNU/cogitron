echo cogitron-record \
    --robot.type=koch_follower \
    --robot.port=$(cogitron-follower-port) \
    --robot.cameras=$(cogitron-camera-config) \
    --robot.id=follower_arm \
    --dataset.repo_id=${HF_USER}/eval-record-test \
    --dataset.single_task="record" \
    --policy.path=${HF_USER}/cogitron-act-policy | bash