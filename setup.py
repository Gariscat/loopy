from setuptools import find_packages, setup


# Required dependencies
required = [
    # Please keep alphabetized
    'librosa>=0.9.2',
    'numpy>=1.19',
    'playsound>=1.3.0',
]


"""# Development dependencies
extras = dict()
extras['dev'] = [
    # Please keep alphabetized
    'ipdb',
    'memory_profiler',
    'pylint',
    'pyquaternion==0.9.5',
    'pytest>=4.4.0',  # Required for pytest-xdist
    'pytest-xdist',
]
"""

setup(
    name='loopy',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    # extras_require=extras,
)