# PyLogBook
A journaling program.

To run:
python PyLogBook.py

# Installing Dependencies

First, create a virtual environment:
`py -m venv venv\`

Then, activate it:
`.\venv\Scripts\activate`

### Pyside6
`pip install Pyside6`

### cryptography
`pip install cryptography`

### PyInstaller
`pip install pyinstaller`

To build the exe file, invoke the `build-exe.ps1` script, from a command-line or PowerShell terminal window, from the source directory.  Note that on Windows 11, it will be necessary to add an exclusion to Windows security for the `build` and `dist` directories.  For more information, see:

[Add an exclusion to Windows Security](https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26#ID0EBF=Windows_11)