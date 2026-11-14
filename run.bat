@echo off
setlocal
cd /d "%~dp0"
call build.bat
if errorlevel 1 exit /b 1
if not exist session mkdir session
if not exist session\companies.csv copy /y data\companies.csv session\companies.csv >nul
if not exist session\companies.csv exit /b 1
cd session
..\build\Karachi_Stock_Simulator.exe
exit /b %errorlevel%
