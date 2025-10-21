# split_dataset.py
import os, random, shutil
from glob import glob

src_pos = "<path>/with_bird"
src_neg = "<path>/no_bird"
dst = "<path>/set"   # will contain train/val/test/with_bird, no_bird

splits = {"train":0.8, "val":0.1, "test":0.1}
os.makedirs(dst, exist_ok=True)
for s in splits:
    for cls in ["with_bird","no_bird"]:
        os.makedirs(os.path.join(dst, s, cls), exist_ok=True)

def split_and_copy(src, cls):
    files = glob(os.path.join(src,"*.*"))
    random.shuffle(files)
    n = len(files)
    i = 0
    for s, frac in splits.items():
        cnt = int(frac * n)
        for f in files[i:i+cnt]:
            shutil.copy(f, os.path.join(dst, s, cls, os.path.basename(f)))
        i += cnt

split_and_copy(src_pos, "with_bird")
split_and_copy(src_neg, "no_bird")
