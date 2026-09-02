# Calibrating Agent-Based Models Workshop

[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22142542.svg)](https://doi.org/10.5281/zenodo.22142542)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JBris/calibrating-abms-workshop.git/HEAD)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Build](https://github.com/JBris/calibrating-abms-workshop/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/JBris/calibrating-abms-workshop/actions/workflows/build.yaml)
[![CodeQL Advanced](https://github.com/JBris/calibrating-abms-workshop/actions/workflows/codeql.yaml/badge.svg?branch=main)](https://github.com/JBris/calibrating-abms-workshop/actions/workflows/codeql.yaml)

[**Documentation**](https://calibrating-abms-workshop.readthedocs.io)
| [**API**](https://calibrating-abms-workshop.readthedocs.io/en/latest/api_reference/index.html)
| [**Changelog**](https://calibrating-abms-workshop.readthedocs.io/en/latest/changelogs/changelog.html)
| [**Releases**](https://github.com/JBris/calibrating-abms-workshop/releases)
| [**Docker**](https://github.com/JBris/calibrating-abms-workshop/pkgs/container/caliagent)
| [**Binder**](https://mybinder.org/v2/gh/JBris/calibrating-abms-workshop.git/HEAD)

*A workshop covering the calibration of agent-based models.*

# Table of contents

- [Calibrating Agent-Based Models Workshop](#calibrating-agent-based-models-workshop)
- [Table of contents](#table-of-contents)
- [Introduction](#introduction)
- [Workshop](#workshop)
- [Usage with Docker](#usage-with-docker)
- [Usage with Binder](#usage-with-binder)
- [Coordinators](#coordinators)
- [Announcements](#announcements)
- [Communication](#communication)
- [Contributions and Support](#contributions-and-support)
- [License](#license)

# Introduction

This repository contains code examples and materials for an introductory session on the calibration of agent-based models (ABMs). The examples are designed to accompany the session and demonstrate, at a high level, what calibration means in the context of ABMs, why calibration is needed, and some of the different approaches that can be used to connect model parameters with observations or other empirical data.

# Workshop

Workshop material for agent-based modelling may be found in the [workshop directory.](docs/source/workshop)

This workshop material includes the following example models:

1. Lotka-Volterra ordinary differential equations
2. Wolf and Sheep Predation agent-based model

We will work though basic examples for optimisation and sensitivity analysis, alongside more complex calibration methods.

# Usage with Docker

To run the examples and workshop material within a Docker container, execute the following:

```
wget https://raw.githubusercontent.com/JBris/calibrating-abms-workshop/refs/heads/main/docker-compose.yaml
docker compose up caliagent

# ctrl + C to exit
```

# Usage with Binder

[Click this link to launch the examples and workshop material within Binder.](https://mybinder.org/v2/gh/JBris/calibrating-abms-workshop.git/HEAD)

Note that you may need to wait roughly 3 or more minutes for the workshop Docker image to be pulled when first using Binder. Please be patient.

# Coordinators

- James Bristow (J.Bristow2@massey.ac.nz)

# Announcements

To view workshop announcements, [please select this link](https://github.com/JBris/calibrating-abms-workshop/tree/main/docs/source/community/announcements.md).

# Communication

Please refer to the following links:

- [GitHub Discussions] for questions.
- [GitHub Issues] for bug reports and feature requests.

[GitHub Discussions]: https://github.com/JBris/calibrating-abms-workshop/discussions
[GitHub issues]: https://github.com/JBris/calibrating-abms-workshop/issues

# Contributions and Support

Contributions are more than welcome. For general guidelines on how to contribute to this project, take a look at [CONTRIBUTING.md](https://github.com/JBris/calibrating-abms-workshop/tree/main/CONTRIBUTING.md).

For our community code of conduct, please also view [CODE_OF_CONDUCT.md](https://github.com/JBris/calibrating-abms-workshop/tree/main/CODE_OF_CONDUCT.md).

# License

This workshop is published under the MIT License (see [LICENSE](https://github.com/JBris/calibrating-abms-workshop/tree/main/LICENSE)).
