<!-- TODO: CHANGE ALL INSTANCES OF "TEMPLATE-README" IN ENTIRE PROJECT TO YOUR PROJECT TITLE-->
# Cogito Cogitron


<div align="center">

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/CogitoNTNU/TEMPLATE-README/ci.yml)
![GitHub top language](https://img.shields.io/badge/languages-Python/C++-orange)
[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue)](https://opensource.org/license/gpl-3-0)
[![Project Version](https://img.shields.io/badge/version-0.0.1-blue)](https://img.shields.io/badge/version-0.0.1-blue)

<img src="https://www.cogito-ntnu.no/cogito_white.svg" width="50%" alt="Cogito Project Logo" style="display: block; margin-left: auto; margin-right: auto;">
</div>

<details> 
<summary><b>📋 Table of contents </b></summary>
  
- [Description](#description)
- [Getting started](#getting-started)
  - [Set up enviroment](#setup-enviroment)
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

If you want to connect to


### Compile
Installing the following packages might be required if they are not present on your machine:
```bash
apt install libcap-dev libsystemd-dev python3-dev
```

You can run the following command to build and install the project. Replace `<wheel-name>` with the generated wheel filename:
```bash
python3 -m build --outdir dist; pip install dist/<wheel-name>.whl --force-reinstall
```

## Scripts
Script for training and running the AI models can be found under the folder:
 ```bash
 ./cogitron/scripts/
 ```

For more information see the [documentation for lerobot](https://huggingface.co/docs/lerobot/il_robots)

### License
------
Distributed under the GPLv3 License. See `LICENSE` for more information.
