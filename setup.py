import setuptools

setuptools.setup(
    name='hls4ml-ipbb',
    version='0.0.1',
    author='Maksymilian Graczyk (CERN)',
    description='An automatic ipbb package for hls4ml IPs',
    package_dir={'': '.'},
    packages=['hls4ml_ipbb'],
    python_requires='>=3.6',
    install_requires=['defusedxml==0.7.1'],
    entry_points={
        'console_scripts': ['ipbb_convert=ipbb_convert:main']
    }
)
