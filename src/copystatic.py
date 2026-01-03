import os
import shutil

def recursive_static_to_docs():
    source_dir = 'static'
    target_dir = 'docs'

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    

    copy_directory(source_dir, target_dir)

def copy_directory(source, target):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        t = os.path.join(target, item)

        if os.path.isdir(s):
            os.makedirs(t, exist_ok=True)
            copy_directory(s, t)
        else:
            shutil.copy2(s, t)
    