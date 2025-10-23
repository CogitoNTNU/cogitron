<!-- TODO: CHANGE ALL INSTANCES OF "TEMPLATE-README" IN ENTIRE PROJECT TO YOUR PROJECT TITLE-->
# Cogito Cogitron


<div align="center">

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/CogitoNTNU/TEMPLATE-README/ci.yml)
![GitHub top language](https://img.shields.io/badge/languages-Python/C-orange)
[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue)](https://opensource.org/license/gpl-3-0)
[![Project Version](https://img.shields.io/badge/version-0.0.1-blue)](https://img.shields.io/badge/version-0.0.1-blue)

<img src="https://www.cogito-ntnu.no/cogito_white.svg" width="50%" alt="Cogito Project Logo" style="display: block; margin-left: auto; margin-right: auto;">
</div>

<details> 
<summary><b>📋 Table of contents </b></summary>
  
- [Description](#description)
- [Getting started](#getting-started)
  - [Set up enviroment](#setup-enviroment)
- [commands](#commands)
- [License](#license)

</details>

## Description 
Longterm robot project created by the members of Cogito Cogitron.

The project is largely inspired by the work done by HuggingFace with [lerobot](https://huggingface.co/docs/lerobot/il_robots).

## Getting started
Prerequisits:
- Ensure that [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/) is installed on your machine. 

Download the repository by running the following:
```bash
git clone https://github.com/CogitoNTNU/cogitron
```

After cloning the repository you can change into the directory by running:
```bash
cd ./cogitron
```

### Connect to existing enviroment
You can search for devices in year network by using the nmap script run by:
```bash
./cogitron/scripts/find_server.sh
```
It is assumed that nmap is installed and that you are running the script in a linux enviroment. If you are on windows you can install WSL and run it from there.

If you get a `Permission denied` error after trying to execute a script you can use the following command to allow execution of the script:
```bash
sudo chmod +x ./cogitron/scripts/find_server.sh
```

After executing the script you will obtain a list of IP-addresses with port 22 open. These will likely have an active SSH-service.

You can connect to a SSH server by running
```bash
ssh cogitron@<ip-address>
```
where you replace the "\<ip-address\>" with the actual ip address you are trying to connect to. You can then type in the password to the SSH session. This gives you a Bash shell to the machine. 

### Setup enviroment on a new machine
Note: It is required to run the code on Linux.

To set up a Python enviroment run the following in the terminal:
```bash
python3 -m venv venv
```

Then activate it:
```bash
. venv/bin/activate
```

Install the requirements with:
```bash
pip install -r requirements.txt
```

If you want to connect to connect to the machine with SSH you have to setup a SSH server on the machine.


### Compile
Installing the following packages might be required if they are not present on your machine:
```bash
apt install libcap-dev libsystemd-dev python3-dev
```

You can run the following command to build and install the project. Replace `<wheel-name>` with the generated wheel filename:
```bash
python3 -m build --outdir dist; pip install dist/<wheel-name>.whl --force-reinstall
```

# Commands
You might need to change the port parameter before running the commands. If all the motors are properly connected you can run:

```bash
cogitron-leader-port
```
```bash
cogitron-follower-port
```

This will find the port for the leader arm and follower arm respectivly. It the scripts does not run successfully, you can use:
```bash
lerobot-find-port
```

Calibrate:
```bash
lerobot-calibrate \
    --robot.type=koch_follower \
    --robot.port=/dev/ttyACM0 \
    --robot.id=follower_arm
```


```bash
lerobot-calibrate \
    --teleop.type=koch_leader \
    --teleop.port=/dev/ttyACM1 \
    --teleop.id=leader_arm
```


Teleoperate:
```bash
lerobot-teleoperate \
--robot.type=koch_follower \
--robot.port=/dev/ttyACM0 \
--robot.id=follower_arm \
--robot.cameras="{ front: {type: opencv, index_or_path: /dev/video0, width: 640, height: 480, fps: 30}}" \
--teleop.type=koch_leader \
--teleop.port=/dev/ttyACM1 \
--teleop.id=leader_arm
```

Record dataset:
```bash
lerobot-record --robot.type=koch_follower --robot.port=/dev/ttyACM0 --robot.id=follower_arm --robot.cameras="{ front: {type: opencv, index_or_path: /dev/video0, width: 640, height: 480, fps: 30}}" --teleop.type=koch_leader --teleop.port=/dev/ttyACM1 --teleop.id=leader_arm --display_data=false --dataset.repo_id=Christiangynnild/record-test --dataset.num_episodes=10 --dataset.single_task=record --dataset.root=dataset --dataset.reset_time_s=15 --dataset.episode_time_s=15
```


Copy files from ssh (change the ip adress to the server ip):
```bash
scp -r cogitron@10.22.22.114:/home/cogitron/cogitron/dataset dataset
```


train policy (Change repo ids):

```bash
lerobot-train \
--dataset.repo_id=christiangynnild/cogitron-act-policy \
--policy.type=act \
--output_dir=outputs/training \
--job_name=cogitron_training \
--policy.device=cuda \
--wandb.enable=true \
--policy.repo_id=christiangynnild/cogitron-act-policy \
--save_freq=1000
```


Evaluate policy (change repo ids):
```bash
lerobot-record  \
  --robot.type=koch_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.cameras="{ front: {type: opencv, index_or_path: /dev/video0, width: 640, height: 480, fps: 30}}" \
  --robot.id=follower_arm \
  --display_data=false \
  --dataset.repo_id=christiangynnild/eval_cogitron-act-policy \
  --dataset.single_task="Put blue cyllinder in box" \
  --policy.path=christiangynnild/cogitron-model-act-policy \
```

Open live camera stream:
```bash
cogitron-video-stream 
```

For more information about possible commands please see the setup.cfg file and the [documentation for lerobot](https://huggingface.co/docs/lerobot/il_robots).


### License
------
Distributed under the GPLv3 License. See `LICENSE` for more information.
