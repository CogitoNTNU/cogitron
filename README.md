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

The project is largely inspired by the work done by HuggingFace with [lerobot](https://github.com/huggingface/lerobot/blob/main/examples/7_get_started_with_real_robot.md).

## Getting started
Prerequisits:
- Ensure that git is installed on your machine. [Download Git](https://git-scm.com/downloads)
- Make sure [Python is installed](https://www.python.org/downloads/).

Download the repository by running the following:
```bash
git clone https://github.com/CogitoNTNU/cogitron
```

After cloning the repository you can change into the directory by running:
```bash
cd ./cogitron
```

### Setup enviroment
Note: It is required to run the code on Linux.

To set up a python enviroment run the following in the terminal:
```bash
python3 -m venv venv
```

Then activate it 
```bash
. venv/bin/activate
```

Install the requirements with:
```bash
pip install -r requirements.txt
```

For more information see the [documentation for lerobot](https://huggingface.co/docs/lerobot/il_robots)


### License
------
Distributed under the GPLv3 License. See `LICENSE` for more information.
