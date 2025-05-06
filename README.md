# substax‑imagery‑tools

Small helper scripts for managing imagery and annotation data in the  
**substax-production-inl** S3 bucket (Idaho National Lab).

## Contents
| File | Purpose |
|------|---------|
| `s3_img_tool.py` | Upload / delete `.tif`, `.tiff`, `.png` files under `imagery/` (flattens paths). |
| `setup_env.bat` | Creates & populates a Conda env (`s3img`) and installs `requirements.txt`. |
| `run_s3_img_tool.bat` | Activates the env and runs `s3_img_tool.py` with any CLI args. |
| `requirements.txt` | Python dependencies (currently just `boto3`). |

## Quick‑start (Windows + Conda)

```bat
REM 1) clone the repo and cd into it
git clone 
cd 

REM 2) one‑time environment setup
setup_env.bat

REM 3) upload a single image
run_s3_img_tool.bat --put dataset/images/substation1/1.tif --profile inl_cli_user

REM 4) bulk‑upload all imagery in a folder (files land in imagery/ with flat names)
run_s3_img_tool.bat --dir dataset/images --profile inl_cli_user

REM 5) delete an object from the bucket
run_s3_img_tool.bat --delete 1.tif --profile inl_cli_user

REM list everything in the bucket
run_s3_img_tool.bat --list --profile inl_cli_user

REM list only under imagery/
run_s3_img_tool.bat --list imagery/ --profile inl_cli_user
```

## CLI reference
| Flag | Description |
|------|---------|
| `--put <FILE>` | Upload one `.tif/.tiff/.png` to `imagery/<basename>` |
| `setup_env.bat` | Creates & populates a Conda env (`s3img`) and installs `requirements.txt`. |
| `run_s3_img_tool.bat` | Activates the env and runs `s3_img_tool.py` with any CLI args. |
| `requirements.txt` | Python dependencies (currently just `boto3`). |