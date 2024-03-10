# Installation

SAPIEN is distributed via [PyPI](https://pypi.org/project/sapien/)

## Dependencies

Python versions:
* Python 3.8, 3.9, 3.10, 3.11, 3.12

Operating systems:
* Linux: Ubuntu 18.04+, Centos 7+
* Windows (experimental): Windows 10,11

Hardware:

* Rendering: NVIDIA or AMD GPU
* Ray tracing: NVIDIA RTX GPU or AMD equivalent
* Ray-tracing Denoising: NVIDIA GPU
* GPU Simulation: NVIDIA GPU

Software:

* Ray tracing: NVIDIA Driver >= 470
* Denoising (OIDN): NVIDIA Driver >= 520

----------

## Install via Pip(PyPI) or Conda

```bash
pip install sapien
```

:::{note}
The pip pacakges requires `pip >= 19.3` to install. Upgrade pip with
```bash
pip install -U pip
```
:::

----------

## Install Nightly Releases 

SAPIEN's latest development version can be accessed through
<https://github.com/haosulab/SAPIEN/releases/tag/nightly>. The builds can be
installed with `pip install {url}` where `url` is the link to the `.whl` file
corresponding to your Python version.

----------

## Build from Source

Since the latest SAPIEN is available through the nightly releases, building
SAPIEN from source should only be needed when building for a unsupported
platform or for development.

### Clone SAPIEN
```bash
git clone --recursive https://github.com/haosulab/SAPIEN.git
cd SAPIEN
```

### Build in Docker
   
While it is possible to build SAPIEN on natively on Linux. We strongly recommend
building using [Docker](https://docs.docker.com/get-started/overview/).

```bash
./docker_build_wheels.sh
```

```{note}

`docker_build_wheels.sh` builds for all Python versions by default. To build for
a specific version, pass the version number (e.g. `./docker_build_wheels.sh 310`
for Python 3.10)
```

### Build natively

For Windows users, SAPIEN should be built directly. Required dependencies
include latest Visual Studio and a Conda environment of desired Python version.

```bash
python setup.py bdist_wheel
```

----------

## Verify Installation

### Server (no display)

```{warning}
This script will generate ``sapien_offscreen.png`` at the current working directory.
```

You may test the offscreen rendering of SAPIEN with the following command

```bash
python -m sapien.example.offscreen
```

On a server without display. It may generate errors about the display. You can
ignore these warnings.

If SAPIEN is installed properly. The following image will be generated at the current working directory, named ``sapien_offscreen.png``.

```{figure} assets/example.offscreen.png
---
width: 120px
align: center
figclass: align-center
---
```

### Desktop (with display)

You may test the onscreen rendering of SAPIEN with the following command

```bash
python -m sapien.example.hello_world
```

This command should open a viewer window showing a red cube on the ground.
