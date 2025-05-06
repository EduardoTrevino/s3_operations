@echo off
REM ---------------------------------------------------------------
REM  setup_env.bat  –  one‑time (or occasional) environment setup
REM ---------------------------------------------------------------
set "ENV_NAME=s3img"

:: Does the env already exist?
conda env list | findstr /I "%ENV_NAME%" >nul
if errorlevel 1 (
    echo === Creating Conda environment "%ENV_NAME%" ...
    conda create -y -n %ENV_NAME% python=3.11
)

echo === Activating "%ENV_NAME%" ...
call conda activate %ENV_NAME%

echo === Installing requirements ...
pip install -r requirements.txt

echo === Environment ready.
