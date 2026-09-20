import os
import shutil
import zipfile
from pathlib import Path

print("[WARN!] DESIGNED FOR STANDARD NATYZ PKGS ONLY !")
print("[WARN!] EXPECTED PKG LAYOUT: [FB].zip/[FB]/[lang]/[lang]_[num].png\n")

os.makedirs("out/zh", exist_ok = True)
os.makedirs("out/en", exist_ok = True)
os.makedirs("out/complex", exist_ok = True)

# 遍历操作包
for zp in Path(".").glob("*.zip"):
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
    
