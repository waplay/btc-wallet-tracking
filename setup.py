
import os
from setuptools import setup, find_packages

from src.version import __version__

# def read_version():
#     with open('btc-wallet-tracking/version.py', 'r') as f:
#         return f.read().strip().split('=')[1].replace("'", "")

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

images = [os.path.join('src/images', img) for img in os.listdir('src/images')]
ui = [os.path.join('src/ui', file) for file in os.listdir('src/ui')]

setup(
    license='MIT',
    name='btc-wallet-tracking',
    version=__version__,
    # py_modules=['main', 'dialog_about', 'dialog_donate', 'dialog_add', 'table_model', 'version'],
    packages=find_packages(),
    include_package_data=True,
    data_files=[('src/images', images), ('src/ui', ui), 'src/wallets.json'],
    entry_points={
        'gui_scripts': [
            'btc-wallet-tracking = src.main:main',
        ],
    },
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)