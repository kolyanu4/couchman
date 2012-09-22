import os, subprocess
from setuptools import setup, find_packages
from distutils.command.build_py import build_py as _build_py

class UiToPy(_build_py):
    def run(self):
        subprocess.check_output(["pyside-uic", "couchman/forms/MainWindow.ui", "-o", "couchman/UI/UI_MainWindow.py"])
        subprocess.check_output(["pyside-uic", "couchman/forms/DB_Manager.ui", "-o", "couchman/UI/UI_DocManager.py"])
        subprocess.check_output(["pyside-uic", "couchman/forms/Server.ui", "-o", "couchman/UI/UI_New_Server.py"])
        subprocess.check_output(["pyside-uic", "couchman/forms/Tasks.ui", "-o", "couchman/UI/UI_New_Task.py"])
        subprocess.check_output(["pyside-uic", "couchman/forms/WorkersWindow.ui", "-o", "couchman/UI/UI_WorkersWindow.py"])
        subprocess.check_output(["pyside-uic", "couchman/forms/ReplicationWindow.ui", "-o", "couchman/UI/UI_ReplicationWindow.py"])
        _build_py.run(self)
        
def read(fname):
    """ Return the text of the file fname """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = "couchman",
    version = "%s-%s" % ("0.4",read("version.txt")),
    description = "derived work of the Krayzman's project https://github.com/kraizman/couchman",
    author = "Nikolay Gavrilyuk",
    author_email = "nikolay.gavrilyuk@smscoin.com",
    url = "https://github.com/kolyanu4/couchman",
    packages = find_packages(),
    cmdclass={'build_py': UiToPy},
    package_data = {
        'couchman': ['media/*'],
    },
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'couchman = couchman.couchman:main',
        ]
    },
    long_description = read('README'),
    classifiers = [
        "Development Status :: 3 - Beta",
        "Topic :: Utilities",
        "License :: GPL License",
    ],
) 
