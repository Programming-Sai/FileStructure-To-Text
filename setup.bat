@echo off
REM Define the installation directory
SET INSTALL_DIR=%ProgramFiles%\FileStructure-To-Text
SET SCRIPT_NAME=ftt
SET PYTHON_SCRIPT_PATH=%~dp0main.py

REM Check if running as administrator
net session >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Please run as Administrator.
    exit /b 1
)

REM Create the installation directory if it does not exist
IF NOT EXIST "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

REM Copy the Python script to the installation directory
copy "%PYTHON_SCRIPT_PATH%" "%INSTALL_DIR%\%SCRIPT_NAME%.py"

REM Create a batch file to run the Python script
echo @echo off > "%INSTALL_DIR%\%SCRIPT_NAME%.bat"
echo python "%INSTALL_DIR%\%SCRIPT_NAME%.py" %%* >> "%INSTALL_DIR%\%SCRIPT_NAME%.bat"

REM Add the installation directory to the PATH
setx PATH "%PATH%;%INSTALL_DIR%"

echo Installation completed successfully.
