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
errfblist = []
badfblist = []


for zp in Path(".").glob("*.zip"):
    ziplist.append(zp)
    if "FB" in zp.name:
        fblist.append(zp)

# count = len(list(root.glob("*.zip")))
print("\t(" + str(len(ziplist)) + ") " + "zip pkgs founded")
print("\t(" + str(len(fblist)) + ") " + "FB pkgs detected")

print("proc pkg layout analyse & transfer ...")
for zip in fblist:
    # check formats
    is_zdlf = False
    ## std ZDLF
    try:
        with zipfile.ZipFile(zip, 'r') as zf:
            dirxt = Path("xt") / zip.stem
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
        print("\t[!] failed in layout analysation: " + zp.name)
        errfblist.append(zp)

    if is_zdlf:
        print("\t" + zp.stem)
            
        # 1-1 xt/ -> dir of extract output
     
        dirxtfb = dirxt / top
            
        # 解压
        with zipfile.ZipFile(zp) as z:
            z.extractall(dirxt)
        print("\t\tok extract")

        # dir paths
        dst_dir_zh = Path(".") / "out" / "zh" / zp.stem
        dst_dir_zh.mkdir(parents=True, exist_ok=True)
        dst_dir_en = Path(".") / "out" / "en" / zp.stem
        dst_dir_en.mkdir(parents=True, exist_ok=True)
        dst_dir_line = Path(".") / "out" / "line" / zp.stem
        dst_dir_line.mkdir(parents=True, exist_ok=True)
        
        # 遍历
        zhcount = 0
        encount = 0
        linecount = 0
            
        # transfer
        # [!] notice the spell-sensitive feature on systems like linux
        if os.path.exists(dirxtfb / "chinese"):
            src_dir_zh = dirxtfb / "chinese"
            for f in src_dir_zh.iterdir():
                if f.is_file():
                    shutil.move(str(f), str(dst_dir_zh / f.name))
                    zhcount = zhcount + 1
            print("\t\tok zh transfer" + " (" + str(zhcount) + ") obj")

        if os.path.exists(dirxtfb / "english"):
            src_dir_en = dirxtfb / "english"
            for f in src_dir_en.iterdir():
                if f.is_file():
                    shutil.move(str(f), str(dst_dir_en / f.name))
                    encount = encount + 1
            print("\t\tok en transfer" + " (" + str(encount) + ") obj")

        if os.path.exists(dirxtfb / "lineart"):
            src_dir_line = dirxtfb / "lineart"
            for f in src_dir_line.iterdir():
                if f.is_file():
                    shutil.move(str(f), str(dst_dir_line / f.name))
                    linecount = linecount + 1
            print("\t\tok line transfer" + " (" + str(linecount) + ") obj")

        # end
        shutil.rmtree(dirxt)
        print("\t\tok xtfb dir cleaned")
        print("\t\tok process")

    else: 
        badfblist.append(zip)

print("bad layout FB pkgs:")
for bad in badfblist:
    print("\t" + bad.stem)