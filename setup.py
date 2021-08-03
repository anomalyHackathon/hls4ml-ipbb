import setuptools

setuptools.setup(
    name='hls4ml-ipbb',
    version='0.0.1',
    author='Maksymilian Graczyk (CERN), Nicolo Ghielmetti (CERN), '
    'Sioni Summers (CERN), and other contributors',
    description='An automatic ipbb package for hls4ml IPs',
    package_dir={'': '.'},
    packages=['hls4ml_ipbb'],
    python_requires='>=3.7',
    install_requires=[
        'defusedxml==0.7.1',
        'numpy==1.21.1',
        'bitstring==3.1.9'
    ],
    entry_points={
        'console_scripts': [
            'ipbb_convert=ipbb_convert:main',
            'numpy_to_mp7=numpy_to_mp7:main'
        ]
    }
)
