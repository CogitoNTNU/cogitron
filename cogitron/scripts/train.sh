lerobot-train \
  --dataset.repo_id=${HF_USER}/cogitron-act-policy \
  --policy.type=act \
  --output_dir=outputs/train/cogitron-act-policy \
  --job_name=cogitron-act-policy \
  --policy.device=cuda \
  --wandb.enable=false \
  --policy.repo_id=${HF_USER}/cogitron-act-policy \
  --save_freq=1 \


