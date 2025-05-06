#!/usr/bin/env python
"""
s3_img_tool.py  –  Minimal helper for substax-production-inl / imagery/

Supported actions
-----------------
--put     <FILE>      upload a single .tif/.tiff/.png ➜ imagery/<basename>
--dir     <FOLDER>    recursively upload *.tif|*.png inside folder tree ➜ imagery/<basename>
--delete  <FILENAME>  delete imagery/<FILENAME> from the bucket
--list    [PREFIX]    list objects (recursively) under bucket/PREFIX  (default = whole bucket)

All uploads flatten the local path; no sub‑directories are created in S3.
"""
from pathlib import Path
import mimetypes, argparse, sys
import boto3

BUCKET          = "substax-production-inl"
DEST_PREFIX     = "imagery/"
ALLOWED_SUFFIX  = (".tif", ".tiff", ".png")

# ── helpers ────────────────────────────────────────────────────────────
def make_client(profile: str | None = None):
    session = boto3.session.Session(profile_name=profile) if profile else boto3
    return session.client("s3")

def content_type(path: Path) -> str:
    return mimetypes.guess_type(str(path))[0] or "binary/octet-stream"

def upload(client, local: Path):
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

def list_objects(client, prefix: str):
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            print(obj["Key"])

# ── CLI ────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None):
    ap = argparse.ArgumentParser(
        description="Upload, delete, or list imagery files in "
                    "substax-production-inl (flattens paths on upload).")
    ap.add_argument("--profile", help="AWS CLI profile name")

    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--put",    metavar="FILE",
                     help="Path to a single .tif/.png to upload")
    grp.add_argument("--dir",    metavar="FOLDER",
                     help="Upload ALL .tif/.png inside folder (recursively)")
    grp.add_argument("--delete", metavar="FILENAME",
                     help="Delete imagery/<FILENAME> (basename only)")
    grp.add_argument("--list",   nargs="?", const="", metavar="PREFIX",
                     help="Recursively list bucket/PREFIX (default entire bucket)")

    args = ap.parse_args(argv)
    cl   = make_client(args.profile)

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

    elif args.list is not None:
        list_objects(cl, args.list)

if __name__ == "__main__":
    main()
