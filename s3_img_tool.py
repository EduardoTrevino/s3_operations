#!/usr/bin/env python
"""
s3_img_tool.py  –  Minimal helper for substax-production-inl / imagery/

USAGE EXAMPLES
--------------

# 1. Single upload
python s3_img_tool.py --put dataset/images/substation1/1.png --profile inl_cli_user

# 2. Upload entire directory tree (flattens names)
python s3_img_tool.py --dir dataset/images --profile inl_cli_user

# 3. Delete unwanted file from bucket
python s3_img_tool.py --delete 1.tif --profile inl_cli_user
"""
from pathlib import Path
import mimetypes
import argparse
import sys
import boto3

BUCKET          = "substax-production-inl"
DEST_PREFIX     = "imagery/"          # all objects land here
ALLOWED_SUFFIX  = (".tif", ".tiff", ".png")

# ── helpers ────────────────────────────────────────────────────────────
def make_client(profile: str | None = None):
    session = boto3.session.Session(profile_name=profile) if profile else boto3
    return session.client("s3")

def content_type(path: Path) -> str:
    return mimetypes.guess_type(str(path))[0] or "binary/octet-stream"

def upload(client, local: Path, profile: str | None = None):
    key = f"{DEST_PREFIX}{local.name}"
    client.upload_file(str(local), BUCKET, key,
                       ExtraArgs={"ContentType": content_type(local)})
    print(f"✓  {local}  →  s3://{BUCKET}/{key}")

def upload_dir(client, folder: Path):
    for f in folder.rglob("*"):
        if f.is_file() and f.suffix.lower() in ALLOWED_SUFFIX:
            upload(client, f)

def delete_obj(client, filename: str):
    key = f"{DEST_PREFIX}{filename}"
    client.delete_object(Bucket=BUCKET, Key=key)
    print(f"✗  deleted  s3://{BUCKET}/{key}")

# ── CLI ────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None):
    ap = argparse.ArgumentParser(
        description="Upload or delete imagery files in substax-production-inl/imagery/ "
                    "(flattens path to filename).")
    ap.add_argument("--profile", help="AWS CLI profile name")

    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--put",    metavar="FILE",
                     help="Path to a single .tif/.png to upload")
    grp.add_argument("--dir",    metavar="FOLDER",
                     help="Upload ALL .tif/.png inside folder (recursively)")
    grp.add_argument("--delete", metavar="FILENAME",
                     help="Delete <FILENAME> from imagery/ (exact basename)")

    args = ap.parse_args(argv)

    cl = make_client(args.profile)

    if args.put:
        p = Path(args.put)
        if not p.is_file():
            sys.exit(f"Error: {p} not found.")
        upload(cl, p)

    elif args.dir:
        d = Path(args.dir)
        if not d.is_dir():
            sys.exit(f"Error: {d} is not a directory.")
        upload_dir(cl, d)

    elif args.delete:
        delete_obj(cl, args.delete)

if __name__ == "__main__":
    main()
