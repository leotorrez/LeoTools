#v 1.3
import os
import re
import argparse

folder_path = "."
def process_folder(folder_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recursive", action="store_true",  default=False)
    args = parser.parse_args()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if args.recursive and os.path.isdir(file_path):
            process_folder(file_path)
        elif filename.endswith('.ini'):
            with open(file_path, "r") as file:
                lines = file.readlines()
            with open(file_path, "w") as file:
                extraFound = False
                for line in lines:
                    if re.search("YelanExtra\]", line):
                        extraFound = True
                    elif re.search("\[", line):
                        extraFound = False
                    if re.search("(^\t?)ps-t1 = ", line):
                        value = line.strip().split(" = ")[1]
                        file.write("if ps-t1 == 943068897\n")
                        if extraFound:
                            file.write("    ps-t1 = ResourceYelanDash\n")
                        else:
                            file.write(";    ps-t1 = ResourceYelanDash\n")
                        file.write("else if ps-t1 != 857068213\n")
                        file.write(f"    ps-t1 = {value}\n")
                        file.write("endif\n")
                    elif re.search("ps-t2 = ", line):
                        file.write("")
                    elif re.search("ps-t3 = ", line):
                        file.write("")
                    elif re.search("; Resources -*$", line):
                        file.write("\n")
                        file.write("[TextureOverrideYelanDash]\n")
                        file.write("hash = 383616e1\n")
                        file.write("filter_index = 943068897\n")
                        file.write("ResourceYelanDash = ps-t1\n")
                        file.write("\n")
                        file.write("[TextureOverrideYelanDash2]\n")
                        file.write("hash = 3315d2b5\n")
                        file.write("filter_index = 857068213\n")
                        file.write("\n")
                        file.write("\n")
                        file.write("; Resources --------------------------- \n")
                        file.write("\n")
                        file.write("[ResourceYelanDash]\n")
                    else:
                        file.write(line)
process_folder(folder_path)
print("Done!")