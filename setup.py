from setuptools import setup

APP = ['main.py']  # Replace with your script's filename
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter'],  # List any additional packages your app uses
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
