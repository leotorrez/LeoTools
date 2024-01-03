'''V 3.0
Speed Control for GI Model Importer mods.'''

import os
import re
import argparse

INI_FILE = "merged.ini"
NEW_INI = "Animation.ini"
sfa, efa = 0, 60
rNum = 0

def dis_ini(file):
    '''Disables the OLD ini by renaming it to DISABLEDmerged.ini'''
    print("Cleaning up and disabling the OLD STINKY ini")
    os.rename(file, os.path.join(os.path.dirname(file), "DISABLED") + os.path.basename(file))

def remER(cln):
    '''Removes all the resources that are not used in the animation'''
    patternDi = re.compile(r"\[Resource(\w+)Diffuse")
    patternLi = re.compile(r"\[Resource(\w+)LightMap")
    patternMi = re.compile(r"\[Resource(\w+)MetalMap")
    patternSi = re.compile(r"\[Resource(\w+)ShadowRamp")
    patternNi = re.compile(r"\[Resource(\w+)NormalMap")
    for i in range(0, len(cln)):
        if "; If you have any issues or find any bugs, please open a ticket at https://github.com/SilentNightSound/GI-Model-Importer/issues or contact SilentNightSound#7430 on discord" in cln[i]:
            break
        if patternDi.match(cln[i]) != None or patternLi.match(cln[i]) != None or patternMi.match(cln[i]) != None or patternSi.match(cln[i]) != None or patternNi.match(cln[i]) != None:
            if cln[i].split(".")[1][0] != f"{rNum}":
                cln[i], cln[i + 1] = "", ""

def textOP(block, si, ei):
    '''Adds the text patch to the animation'''
    corPatch = "if $swapvar >= $frameStart && $swapvar <= $frameEnd\n"
    global rNum
    for i in range(si + 3, ei):
        if "else if $swapva" in block[i]:
            break
        corPatch += f"{block[i]}"
    for i in range(si, ei):
        if "ps-t" in block[i]:
            block[i] = ""
    block[si] += f"{corPatch}endif\n"
    rNum = corPatch.split(".")[1][0]

def text_ini(file):
    '''Adds the text patch to the animation'''
    fc = []
    patternH = re.compile(r"\[CommandList(\w+)Head")
    patternB = re.compile(r"\[CommandList(\w+)Body")
    patternD = re.compile(r"\[CommandList(\w+)Dress")
    patternE = re.compile(r"\[CommandList(\w+)Extra")

    with open(file, "r", encoding="utf-8") as f:
        fc = f.readlines()
        flagen = ""
        for i, line in enumerate(fc):
            if patternH.match(line) and "Face" not in line:
                flagen = "head"
                si = i
            elif patternB.match(line):
                flagen = "body"
                si = i
            elif patternD.match(line):
                flagen = "dress"
                si = i
            elif patternE.match(line):
                flagen = "extra"
                si = i
            elif "endif" in line and flagen != "":
                textOP(fc, si, i)
                flagen = ""
    remER(fc)
    with open(NEW_INI, "w", encoding="utf-8") as f:
        f.writelines(fc)

def speed_ini(file, sfa, efa):
    '''Adds the speed control to the animation'''
    fc = []
    with open(file, "r", encoding="utf-8") as f:
        fc = f.readlines()
        for i in range(0, len(fc)):
            if f'; Overrides ---------------------------' in fc[i]:
                    DelIndex = i
                    break
        for i in range(5, DelIndex - 1):
             fc.pop(5)
        fc[5] = f'''global $fps = 60
global $frameStart= {sfa}
global $frameEnd = {efa}
global $swapvar = 0
global $active = 0
global $creditinfo = 0

'''
        fc.insert(6, '''[Present]
$swapvar = (time * $fps % ($frameEnd - $frameStart + 1) + $frameStart) // 1

''')        
    dis_ini(INI_FILE)
    with open(NEW_INI, "w", encoding="utf-8") as f:
        f.writelines(fc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Modifies the auto-generated merged.ini to apply patches needed for animation")
    parser.add_argument("-s", "--startFrame", type=int, help="The starting frame")
    parser.add_argument("-e", "--endFrame", type=int, help="The ending frame")
    parser.add_argument("-f", "--file", type=str, help="The file to be modified")
    parser.add_argument("-o", "--output", type=str, help="The output file")
    args = parser.parse_args()
    if args.startFrame:
        sfa = args.startFrame
    if args.endFrame:
        efa = args.endFrame
    if args.file:
        INI_FILE = args.file
    if args.output:
        NEW_INI = args.output
    speed_ini(INI_FILE, sfa, efa)
    text_ini(NEW_INI)
