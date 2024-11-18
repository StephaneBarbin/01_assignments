:: ******************************************************************
:: Batch to start Maya
:: Stephane Barbin
::*******************************************************************

@echo off

:: MAYA
set "MAYA_VERSION=2023"
set "MAYA_PATH=C:\Program Files\Autodesk\Maya%MAYA_VERSION%"


:: PATH
set "SCRIPT_PATH=F:\_python\02_python_advanced\01_work\00_project\scripts"
set "PYTHONPATH=%SCRIPT_PATH%;%PYTHONPATH%"


:: PLUGIN
set "MAYA_PLUGIN_PATH=%SCRIPT_PATH%\plugins;%MAYA_PLUGIN_PATH%"


:: SHELF
set "MAYA_SHELF_PATH=%SCRIPT_PATH%\shelf;%MAYA_SHELF_PATH%"


:: SPLASHSCREEN
set "XBMLANGPATH=%SCRIPT_PATH%\img;%XBMLANGPATH%"


:: DISABLE REPORT
set "MAYA_DISABLE_CIP=1"
set "MAYA_DISABLE_CER=1"


:: MAYA
start "" "%MAYA_PATH%\bin\maya.exe"

exit