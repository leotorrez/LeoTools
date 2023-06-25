import os
import re
import configparser
import argparse

ini_file = "merged.ini"
rNum = 0

# Diabling the OLD ini
def dis_ini(file):
    print("Cleaning up and disabling the OLD STINKY ini")
    os.rename(file, os.path.join(os.path.dirname(file), "DISABLED") + os.path.basename(file))

def remER(cln):
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
    corPatch = "if $swapvar >= $frameStart && $swapvar <= $frameEnd\n"
    global rNum
    for i in range(si + 3, ei):
        if "else if $swapva" in block[i]:
            break
        corPatch += f"{block[i]}"

    for i in range(si, ei):
        if "ps-t" in block[i]:
            block[i] = ""
    block[si] += f"{corPatch}\nendif\n"
    rNum = corPatch.split(".")[1][0]


def text_ini(file):
    fc = []
    patternH = re.compile(r"\[CommandList(\w+)Head")
    patternB = re.compile(r"\[CommandList(\w+)Body")
    patternD = re.compile(r"\[CommandList(\w+)Dress")
    patternE = re.compile(r"\[CommandList(\w+)Extra")

    with open(file, "r", encoding="utf-8") as f:
        fc = f.readlines()
        flagen = ""
        
        for i in range(0, len(fc)):
            if patternH.match(fc[i]) != None and "Face" not in fc[i]:
                #print("head",fc[i],i)
                flagen = "head"
                si = i
            elif patternB.match(fc[i]) != None:
                #print("body",fc[i],i)
                flagen = "body"
                si = i
            elif patternD.match(fc[i]) != None:
                #print("dress",fc[i],i)
                flagen = "dress"
                si = i
            elif patternE.match(fc[i]) != None:
                #print("extra",fc[i],i)
                flagen = "extra"
                si = i
            elif "endif" in fc[i] and flagen != "":
                textOP(fc, si, i)
                flagen = ""
                
#        for i in range(5, DelIndex - 1):
#             fc.pop(5)
#        fc[5] = f'global $speed = 0.5\nglobal $frameStart= 0\nglobal $frameEnd = 60\nglobal $swapvar = 0\nglobal $auxTime = 0\n\n'
#        fc.insert(6, f'[Present]\nif $auxTime % $speed == 0\n    if $swapvar < $frameEnd\n        $swapvar = $swapvar + 1\n    else\        $swapvar = $frameStart\n    endif\nendif\nif $auxTime >= 1000\n    post $auxTime = $auxTime - 1000\nelse\n    post $auxTime= $auxTime + 1\nendif\n\n')

    remER(fc)

    with open('0.ini', "w", encoding="utf-8") as f:
        f.writelines(fc)



def speed_ini(file, sfa, efa):
    fc = []
    with open(file, "r", encoding="utf-8") as f:
        fc = f.readlines()
        for i in range(0, len(fc)):
            if f'; Overrides ---------------------------' in fc[i]:
                    DelIndex = i
                    break
        for i in range(5, DelIndex - 1):
             fc.pop(5)
        fc[5] = f'global $speed = 0.5\nglobal $frameStart= {sfa}\nglobal $frameEnd = {efa}\nglobal $swapvar = 0\nglobal $auxTime = 0\n\n'
        fc.insert(6, f'[Present]\nif $auxTime % $speed == 0\n    if $swapvar < $frameEnd\n        $swapvar = $swapvar + 1\n    else\n        $swapvar = $frameStart\n    endif\nendif\nif $auxTime >= 1000\n    post $auxTime = $auxTime - 1000\nelse\n    post $auxTime= $auxTime + 1\nendif\n\n')
        
    dis_ini(ini_file)
    with open('0.ini', "w", encoding="utf-8") as f:
        f.writelines(fc)

parser = argparse.ArgumentParser(description="Modifies the auto-generated merged.ini to apply patches needed for animation")
parser.add_argument("-s", "--startFrame", type=int, help="The starting frame")
parser.add_argument("-e", "--endFrame", type=int, help="The ending frame")
args = parser.parse_args()
sfa, efa = 0, 60
if args.startFrame:
    sfa = args.startFrame
if args.endFrame:
    efa = args.endFrame
speed_ini(ini_file, sfa, efa)
text_ini("0.ini")
