import glob
import os
import shutil
import sys
import subprocess

curpath = os.path.dirname(os.path.realpath(__file__))
appsrcopyFilesath = os.path.join(curpath, "src", 'roam')




def buildqtfiles():
    def _hashcheck(file):
        import hashlib
        hasher = hashlib.md5()
        with open(file, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        hash = hasher.hexdigest()
        filehash = hashes.get(file, "")
        hashes[file] = hash
        if hash != filehash:
            print("Hash changed for: {0}, Got {2} wanted {1}".format(file, hash, filehash))
            return False
        else:
            return True


    import json
    hashes = {}
    try:
        with open(".roambuild") as f:
            hashes = json.load(f)
    except Exception:
        hashes = {}

    HASHFILES = [".ui", ".ts"]
    for folder in [appsrcopyFilesath]:
        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                file, ext = os.path.splitext(filepath)

                #if ext in HASHFILES and _hashcheck(filepath):
                #    print(f"Skipping {file} - Hash match")
                #    continue

                if ext == '.ui':
                    newfile = file + ".py"
                    # compile the ui file with subprocess
                    print(f"Compiling {newfile}")
                    cmd = ['pyuic5', '-o', newfile, filepath]
                    print(' '.join(cmd))
                    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    stderr, stdout = p1.communicate()
                    print(str(stderr))
                elif ext == '.qrc':
                    newfile = file + "_rc.py"
                    p1 = subprocess.Popen(['pyrcc5', '-o', newfile, filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    p1.communicate()	
                elif ext == '.ts':
                    newfile = file + '.qm'
                    try:
                        p1 = subprocess.Popen(['lrelease', '-o', newfile, filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        p1.communicate()
                    except:
                        print("Missing lrelease - skipping")
                        continue

    with open(".roambuild", "w") as f:
        json.dump(hashes, f)

buildqtfiles()