import os
import re

ini_file = "merged.ini"

# Diabling the OLD ini
def dis_ini(file):
    print("Cleaning up and disabling the OLD STINKY ini")
    os.rename(file, os.path.join(os.path.dirname(file), "DISABLED") + os.path.basename(file))

def read_ini(file):
    fc = []
    with open(file, "r", encoding="utf-8") as f:
        fc = f.readlines()
        for i in range(0, len(fc)):
            if f'; Overrides ---------------------------' in fc[i]:
                    DelIndex = i
                    break
        for i in range(5, DelIndex - 1):
             fc.pop(5)
        fc[5] = f'global $ActiveCharacter = 0\nglobal $speed = 0.5\nglobal $frameStart= 0\nglobal $frameEnd = 60\nglobal $swapvar = 0\nglobal $auxTime = 0\n\n'
        fc.insert(6, f'[Present]\nif $auxTime % $speed == 0\n    if $swapvar < $frameEnd\n        $swapvar = $swapvar + 1\n    else\n        $swapvar = $frameStart\n    endif\nendif\npost $auxTime=$auxTime+1\n\n')
    
    with open('Anim.ini', "w", encoding="utf-8") as f:
        f.writelines(fc)

read_ini(ini_file)
dis_ini(ini_file)