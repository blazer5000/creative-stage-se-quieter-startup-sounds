@echo off
setlocal
if "%~1"=="" (
  echo Drag "Creative Stage SE FW Update v1001.zip" onto this file.
  echo.
  pause
  exit /b 1
)
py -3 "%~dp0make_quieter_firmware.py" "%~1"
echo.
pause
