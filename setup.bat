@echo off
REM Define the installation directory and script details
SET "INSTALL_DIR=%ProgramFiles%\FileStructure-To-Text"
SET "SCRIPT_NAME=ftt"
SET "PYTHON_SCRIPT_PATH=%~dp0main.py"

REM Create the installation directory if it does not exist
IF NOT EXIST "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

REM Copy the Python script to the installation directory
copy "%PYTHON_SCRIPT_PATH%" "%INSTALL_DIR%\%SCRIPT_NAME%.py"

REM Create a batch file to run the Python script
echo @echo off > "%INSTALL_DIR%\%SCRIPT_NAME%.bat"
echo python "%INSTALL_DIR%\%SCRIPT_NAME%.py" %%* >> "%INSTALL_DIR%\%SCRIPT_NAME%.bat"

REM Add the installation directory to the PATH environment variable
setx PATH "%PATH%;%INSTALL_DIR%"

REM Confirm the PATH update and check the installation
echo Installation completed successfully.
echo Please open a new Command Prompt to use the 'ftt' command.
pause
