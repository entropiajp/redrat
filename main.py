import os
import argparse
import subprocess

from tqdm import tqdm

parser = argparse.ArgumentParser(
    prog='redrat',
    add_help=True
)

parser.add_argument('container')
parser.add_argument('volume_id')
parser.add_argument('root_path')

input_args = parser.parse_args()
CONTAINER = input_args.container
VOLUME_ID = input_args.volume_id
ROOT_PATH = input_args.root_path


def ls(path):
    dirs = []
    files = []
    args = ['./drat', 'list', CONTAINER, VOLUME_ID, path]
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode == 0:
        lines = p.stderr.decode("utf-8")
        for ln in lines.split("\n"):
            if ln.find("- DIR REC") >= 0:
                parts = ln.split(" || ")
                if len(parts) >= 4:
                    name = parts[-1].split(" = ")[-1]
                    if parts[1] == "Dirctry":
                        dirs.append(name)
                    else:
                        files.append(name)
    else:
        print("\n" + " ".join(args))
    return [dirs, files]

def scan(path):
    file_paths = []
    dirs, files = ls(path)
    if path == '/':
        path = ''
    for f in files:
        file_paths.append(path + "/" + f)

    for d in dirs:
        s = path + "/" + d
        file_paths += scan(s)
    
    return file_paths

def recover(paths):
    for path in tqdm(paths, unit="file"):
        dest_path = "./" + path[1:]
        d = os.path.dirname(dest_path)
        if not os.path.isdir(d):
            os.seteuid(501)
            os.makedirs(d)
            os.seteuid(0)
        args = ['./drat', 'recover', CONTAINER, VOLUME_ID, path]
        p = subprocess.run(args, capture_output=True)
        outfile = open(dest_path, "wb")
        outfile.write(p.stdout)
        outfile.close()


print("[redrat] Collecting filepaths...")
paths_list = scan(ROOT_PATH)
recover(paths_list)
