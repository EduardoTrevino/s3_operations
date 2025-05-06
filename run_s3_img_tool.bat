@echo off
REM ---------------------------------------------------------------
REM  run_s3_img_tool.bat  –  execute s3_img_tool.py with env active
REM ---------------------------------------------------------------
set "ENV_NAME=s3img"

call conda activate %ENV_NAME%
python s3_img_tool.py %*
