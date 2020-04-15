"Program to build project into exexutable and installer"
import sys
from cx_Freeze import setup, Executable
import os.path

if 'bdist_msi' in sys.argv:
    PATH = "C:\Program Files\Tetris"
    #sys.argv += ['--initial-target-dir', PATH]

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Tetris",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]main.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     "icon.ico",                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

base = None
if sys.platform == "win32": base = "Win32GUI"

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

executables = [Executable(script="main.py", base=base)]

setup(
    name = 'Tetris',
    author = 'Ethan Armstrong',
    options={
        "build_exe": {
            "packages":["pygame", "os", "sys", "random"],
            "include_files":["hs.txt", "b.png", "bP.png", "icon.ico"],
            },
        "bdist_msi": bdist_msi_options,
    },
    executables = executables,
    version = "1.0"
)
