# hls4ml-ipbb

A Python 3 package for producing ipbb-compatible wrappers of hls4ml IPs, along with easy-to-use `ipbb_convert` and `numpy_to_mp7` command-line scripts.

## Installation
In all cases, make sure your Python environment is the one you want to set up `hls4ml-ipbb` in.

### git
Clone this repository and run the following command inside your newly-created repository folder:
```
pip install -e .
```
If you want to make changes to the code (e.g. tweak the VHDL wrapper template for your use case), you can do so directly in the repository folder.

## How to use
`hls4ml-ipbb` takes an hls4ml project and produces an ipbb component directory that you can use in your project using ipbb, e.g. an [emp-fwk](https://gitlab.cern.ch/p2-xware/firmware/emp-fwk) project (a CERN account required).

Before using the package, make sure that an hls4ml project to be converted has the exported IP (this can be done by running an appropriate feature in your HLS software, e.g. "Export RTL" in Vivado HLS).

### Quick start: ipbb_convert
The easiest way to start working with `hls4ml-ipbb` is using the provided `ipbb_convert` script.

**To convert an hls4ml project stored in folder A to an ipbb component to be stored in folder B, run:**
```
ipbb_convert A B
```
That's it! If a directory B does not exist, it will be automatically created.

`ipbb_convert` has a few extra options that can or must be used, depending on your use case (e.g. the name of an HLS solution to be processed). Run `ipbb_convert -h` for the extensive help message.

### Advanced: hls4ml_ipbb Python module
If you want to integrate `hls4ml-ipbb` into your Python project, you can do it by using the `hls4ml_ipbb` module. All public classes and methods should be either documented with docstrings or self-explanatory (if a subclass does not have docstrings, try looking for them in its parent class).

Here is a short example of how to use `hls4ml_ipbb` to convert an hls4ml project with a Vivado HLS solution called "solution1":
```python3
import hls4ml_ipbb

project = hls4ml_ipbb.Project('<path to your hls4ml project>',
                              backend=hls4ml_ipbb.backend.VivadoBackend())
ip = project.get_ip('solution1')
wrapper = hls4ml_ipbb.VHDLWrapper(ip)
wrapper.save('<path to a directory where the ipbb component should be created>')
```

### numpy_to_mp7
`hls4ml-ipbb` includes also a small script `numpy_to_mp7` designed for converting numpy files to the format recognisable by boards using ipbb (e.g. [Imperial MP7](http://www.hep.ph.ic.ac.uk/mp7/)).

(under construction)

## Supported HDLs and HLS software
Only VHDL and Vivado HLS are supported at the moment. However, `hls4ml-ipbb` is designed with extensibility in mind, so if you need support of a different HDL or HLS software and you are comfortable with Python 3, feel free to contribute!
