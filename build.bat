@echo off
setlocal
cd /d "%~dp0"
if not exist build mkdir build
where cl >nul 2>nul
if not errorlevel 1 goto msvc
set "INSTALLER=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer"
if not exist "%INSTALLER%\vswhere.exe" goto mingw
pushd "%INSTALLER%"
for /f "delims=" %%I in ('vswhere.exe -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath') do set "VCVARS=%%I\VC\Auxiliary\Build\vcvars64.bat"
popd
if not defined VCVARS goto mingw
call "%VCVARS%" >nul
if not errorlevel 1 goto msvc
:mingw
where g++ >nul 2>nul
if errorlevel 1 (
    echo Install MSVC C++ Build Tools or add MinGW-w64 g++ to PATH.
    exit /b 1
)
g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic -static src\market_simulator.cpp -o build\Karachi_Stock_Simulator.exe -luser32
exit /b %errorlevel%
:msvc
cl /nologo /EHsc /std:c++17 /utf-8 /W4 /O2 /Fo:build\market_simulator.obj /Fe:build\Karachi_Stock_Simulator.exe src\market_simulator.cpp /link user32.lib
exit /b %errorlevel%
