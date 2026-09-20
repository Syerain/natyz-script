import os
import zipfile
import shutil
from pathlib import Path

print("[*] Natyz Script\n\tdev by Syerain\n\tgithub.com/Syerain/natyz-script\n\tlicense: CC0")
print("[*] supported working mode: ZDLF, ZDDLF, X, complex;")

print("checking pkgs ...")

root = Path(".")

zipcount = 0
fbcount = 0

ziplist = []
fblist = []


for zp in Path(".").glob("*.zip"):
    ziplist.append(zp)
    if "FB" in zp.name:
        fblist.append(zp)

# count = len(list(root.glob("*.zip")))
print("\t(" + str(len(ziplist)) + ") " + "zip pkgs founded")
print("\t(" + str(len(fblist)) + ") " + "FB pkgs detected")

for zip in fblist:
    # check formats
    print("proc pkg layout analyse & transfer ...")
    is_zdlf = False
    ## std ZDLF
    try:
        with zipfile.ZipFile(zip, 'r') as zf:
            dir = Path("xt") / zip.stem
            #zf.extractall(dir)
            names = zf.namelist()

            # D
            depth1 = set()
            for n in names:
                parts = n.split('/')
                if parts[0]:
                    depth1.add(parts[0])
            is_single_depth1 = len(depth1) == 1
            top = list(depth1)[0] if is_single_depth1 else None

            # L
            has_en_dir = False
            dir_prefix_english = None
            if is_single_depth1:
                dir_prefix_english = top + '/english'
                for n in names:
                    if n.startswith(dir_prefix_english):
                        has_en_dir = True
                        break

            # final
            if is_single_depth1 and has_en_dir:
                is_zdlf = True

    except Exception as e:
        print("\t[!] failed to analyse pkg as ZDLF layout: " + zp.name)

    if is_zdlf:
        print(zp.stem + "\non process:")
            
        # 1-1 xt/ -> dir of extract output
        dir = Path("xt") / zp.stem
        dir.mkdir(parents=True, exist_ok=True)
            
        # 解压
        with zipfile.ZipFile(zp) as z:
            z.extractall(dir)
        print("\tok extract")
        
          # 目录
          # [!] notice the spell-sensitive feature on systems like linux
        src_dir_zh = next(dir.glob("*/chinese"))
        src_dir_en = next(dir.glob("*/english"))
        dst_dir_zh = Path(".") / "out" / "zh" / zp.stem
        dst_dir_zh.mkdir(parents=True, exist_ok=True)
        dst_dir_en = Path(".") / "out" / "en" / zp.stem
        dst_dir_en.mkdir(parents=True, exist_ok=True)
        
        # 遍历
        zhcount = 0
        encount = 0
            
        ## zh
        for f in src_dir_zh.iterdir():
            if f.is_file():
                shutil.move(str(f), str(dst_dir_zh / f.name))
                zhcount = zhcount + 1
        print("\tproc: " + str(zhcount) + " img transfered")
        print("\tok zh transfer")
            
        ## en
        for f in src_dir_en.iterdir():
            if f.is_file():
                shutil.move(str(f), str(dst_dir_en / f.name))
                encount = encount + 1            
        print("\tproc: " + str(encount) + " img transfered")
        print("\tok en transfer")
        
        # 收尾
        print("\tok process")
