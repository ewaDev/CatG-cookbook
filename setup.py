"""
Scrip for converting the CatG.py script to an executable
Author: Ewa G
Date: 08/09/2017
"""

from cx_Freeze import setup, Executable
import os
import sys

####code taken from https://stackoverflow.com/questions/35533803/keyerror-tcl-library-when-i-use-cx-freeze
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


base = None
if sys.platform == "win32":
    base = "Win32GUI"

options = {
     'build_exe': {
    'include_files':[
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
     ],
} }

setup(
    name = "CatG_program",
    version = "1.0",
    description = "Microarray",
    options = options,
    executables = [Executable( "catG.py", base=base)],

)
