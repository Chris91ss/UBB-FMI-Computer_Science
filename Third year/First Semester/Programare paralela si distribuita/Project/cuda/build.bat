@echo off
REM Build CUDA n-body simulation
echo Building CUDA n-body simulation...

call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"

if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to set up Visual Studio environment
    pause
    exit /b 1
)

nvcc -O3 -arch=sm_75 -std=c++11 -o nbody_cuda.exe main.cu nbody_cuda.cu

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build successful! nbody_cuda.exe created.
    echo.
) else (
    echo.
    echo Build failed!
    echo.
    pause
    exit /b 1
)

pause

