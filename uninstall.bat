@echo off
REM Define the installation directory
SET INSTALL_DIR=%ProgramFiles%\FileStructure-To-Text
SET SCRIPT_NAME=ftt

REM Check if running as administrator
net session >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Please run as Administrator.
    exit /b 1
)

REM Remove the Python script and batch file
del "%INSTALL_DIR%\%SCRIPT_NAME%.py"
del "%INSTALL_DIR%\%SCRIPT_NAME%.bat"

REM Remove the installation directory if it is empty
rmdir "%INSTALL_DIR%"

REM Remove the installation directory from the PATH
setx PATH "%PATH:;%INSTALL_DIR%;%"

echo Uninstallation completed successfully.
