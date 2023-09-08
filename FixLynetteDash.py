# V2.3

# fixed Lynette Dash fix
# original script https://github.com/leotorrez/LeoTools/blob/main/FixLynetteDash.py
# fixed by z3phyn 

# original fix https://discord.com/channels/971945032552697897/995556578675671121/1149641642505142312
# fixed fixed by LeoTorreZ <3 Thanks Zlevir for playtesting

import os
import re
import argparse

folder_path = "."
def process_folder(folder_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recursive", action="store_true",  default=False)
    args = parser.parse_args()
    for filename in [filename for filename in os.listdir(folder_path) if "disabled" not in filename.lower()]:
        file_path = os.path.join(folder_path, filename)
        disabled_path = os.path.join(folder_path, "DISABLED_brokendash" + filename)
        
        if args.recursive and os.path.isdir(file_path):
            process_folder(file_path)
        elif filename.endswith('.ini'):
            with open(file_path, "r") as file:
                lines = file.readlines()
            os.rename(file_path, disabled_path)
            with open(file_path, "w") as file:
                bodyFound = False
                extraFound = False
                firstShaderReplace = True
                for line in lines:
                    if re.search("LynetteExtra\]", line):
                        bodyFound = False
                        extraFound = True
                    elif re.search("LynetteBody\]", line):
                        bodyFound = True
                        extraFound = False
                    elif re.search("\[", line):
                        bodyFound = False
                        extraFound = False
                    if re.search("(^\t?)ps-t1 = ", line):
                        value = line.strip().split(" = ")[1]
                        file.write("if ps-t1 == 943068897\n")
                        if extraFound:
                            file.write("    ps-t1 = ResourceLynetteDash\n")
                        else:
                            file.write(";    ps-t1 = ResourceLynetteDash\n")
                        file.write("else if ps-t1 != 857068213\n")
                        file.write(f"    ps-t1 = {value}\n")
                        if not (bodyFound or extraFound):
                            file.write("endif\n")
                    elif re.search("ps-t2 = ", line):
                        if bodyFound or extraFound:
                            value = line.strip().split(" = ")[1]
                            file.write(f"    ps-t2 = {value}\n")
                            file.write("endif\n")
                    elif re.search("ps-t3 = ", line):
                        file.write("")
                    elif re.search(" = reference", line):
                        if "Head" in line or "Dress" in line:
                            line = line.replace("ps-t1", "ps-t0")
                            line = line.replace("ps-t2", "ps-t1")
                        file.write(line)
                    elif re.search("\[ShaderRegexCharReflection\]", line) and firstShaderReplace == True:
                        firstShaderReplace=False
                        file.write(
r"""[ShaderOverrideSprint]
hash = fd8af14fb718d258
run = CommandListSprint
allow_duplicate_hash=overrule

[CommandListSprint]
if $CharacterIB != 0
    if $CharacterIB == 1
        ps-t0 = copy ResourceRefHeadLightMap
    else if $CharacterIB == 2
        ps-t0 = copy ResourceRefBodyDiffuse
    else if $CharacterIB == 3
        ps-t0 = copy ResourceRefDressLightMap
    else if $CharacterIB == 4
        ps-t0 = copy ResourceRefExtraDiffuse    
    endif
drawindexed=auto
$CharacterIB = 0
endif

[TextureOverrideLynetteDash]
hash = b3aaa524
match_priority = 65465
filter_index = 943068897
ResourceLynetteDash = ps-t1

[ResourceLynetteDash]

[ShaderRegexCharReflection]
""")
                    else:
                        file.write(line)
            with open(file_path, 'r') as f:
                s = f.read()
            s = s.replace(r"""[ShaderRegexCharOutline]
shader_model = ps_5_0
run = CommandListOutline
[ShaderRegexCharOutline.pattern]
mov o\d+\.\w+, l\(\d+\)\n
mov o\d+\.\w+, r\d+\.\w+\n
mov o\d+\.\w+, l\(\d+\.\d+\)
""", r"""[ShaderOverrideOutline]
hash=6ce92f3bcc9c03d0
run = CommandListOutline
allow_duplicate_hash=overrule""")
            with open(file_path, 'w') as f:
                f.write(s)

if __name__ == "__main__":
    prompt = input("This script will fix Lynette Dash for you. YOU MUST run AGMG3ShaderFix 37.py before hand. Do you want to continue? (y/n) ")
    if prompt.lower() == "y":
        process_folder(folder_path)
        print("Done! Make sure to install Yelan Dash fix in ShaderFixes")
    else:
        print("Canceled. Exiting...")