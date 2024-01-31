# Made by LeoTorreZ and SilentNightSound
# Immense thanks to the Genshin Impact Modding Community for their help and support
# Specially Gustav0, Zlevir and SinsofSeven for their aid on getting the resources and testing

# Fixes Bennett, Cyno, Fischl, Kirara, Mona/MonaCN, Nahida, Razor, Xinyan, Amber/AmberCN, Ningguang, Venti, Diluc and Xiao
# Note: This fix DOES NOT contain the 4.1 and 4.3 fixes - for older mods, run 4.3 first before this one

# ################################################################################
#                            .........
#                        :+#%@@@@@@%%@@%#+-.
#                  .. =%@@@%@*##*##*%#%@@@@@@@+-*:
#                .**%@@@@@@%*+*%@#*+#%@@@@@@@@@#*##:.
#               .*%#@@@@@@@@@@%##%@@@@@@@@@@#*+#*#%*#-
#              :=###@@@@*+*##+###@@*-=++++*#@****####%*+.
#             .++###@@*#@@@@@@%+#*+@@@@@@@@@#=@+###*#%*#@#:
#             .++##*@#+=-==+*%@@+#@@@@@@@@%+*%=###+##%:..:*=.
#             .:+=#*@+-:-=*###+*@@#+++==**=--=%##+###::::+:**
#            .:.-=++:+@@@@@@%*+*#@%##%@@@@@@@%==*##-.:+=+#::@=
#            :@@@@@@@@@@@%*#%#%@@@@@@@@%##%@@@@@%##**#+-*+*:##.
#             -@@@@@@@@%*@@@#@@@@@@@@@@@@@@%*%@@@@@@@*-:*::.*-
#            .-++#@@@@##@@@#%@@@@@@@@@@@@@@@@%+%@@@%#-#@=.:.-.
#           .+%@@@@@@**@@@@#@@@@@@@@@@@@@@@@@@@%#@@@@@**@@+..
#          :#@@@@@@@##@@@@%#@@@@@@@@@@@@@@@@@@@@%*@@@@@#*@@%.
#         .%@@@@@@@*%@@@@@%%@@@@@@@@@@@@@@@@@@%@@@*@@@@@*#@@#.
#        :%@@@@@###@@@@@@@%%@@@@@@@%@%@@@@@@@@@@@@%#@@@@@*%@@=
#       .*@@@@@#*@@@%@@@@@%#@@@@@@@@@%@@@@@@@@@@@@@##@@@@@*%@*.
#       -%@@@@@@@%##*@@@@@%#@@@@@@@@%*@@@@@@@@@@@@@%+@@@@@%*@#.
#      .+@@@@@@@@@@%+@@@@@@#@@@%@@@@#-#@@%%@@@@@@@@@**@@@@@#+*:
#      .#@@@@@@@@@@%=*@@@@@#%@@@@@@@-%=%@@*%@@@@@@@@@=%@@@@@@*:.
#      :@@@@@@@@@@@*#*#@@@@@*@@@@@%=@@@=#@%*@@%@@@@@@%#%*#%@@@@@-
#    .-@@@@@%@@@@@#+##+%@@@@##@@@%+****#+#@**@@#%@@@@@##@@%#===-.
# .-*%@@@@%*%@@@@+%@@@%+#@@@@#%@*+@@@@@@@#+@*%@@%+%@@@@*#@@@@+=++.
#   =**==*#%@@@#*@@%#+#+%+%@@@*==@@####%%@@**#@@@@%=*%@@@*#@@%++++-.
#     .*%#@@%#+=%=:----+*#%*%@@*%@@%=-=--:-=**@@@@@+%@%%%%@%%%%:
#    .+%%%%%%%@*--*+*-==*%*@%*+#%#%:=--++*%=:+@@@@@*%%%@%%%%####.
#  .:+*##%%*+@+--%@++=#++%=++%#=%@%==**=*+@*==@@@@@*@%+++*++**+++-..
#  :---****##%+-+@@%++++*@=-=---*@@*+-=*+*@===@@@@%*@@*=*++**-::-::.
#      ...   *%--+%@#++#@#-#@%*-*@@@=-=-*@#---@@@@*=%@@*++=.
#            :@#-=%@%%@%+-#@@@@#:+@@@@@@@#:--=%%@#-+=::-:+++:
#             -%#:---==+#@@%###@@*--+*+=---==+%%*-+=:
#              :#=-+=.-=+*%%@@@@@%%*=-:-=+===##-:+++=.
#                :-:.  .:--:..:-:::::=*+-.-*=.     ...
#                       -%@#*:===:++=@@@#=.:=*:
#                      :%@#=:-+=----%@@@@#:.=%%.
#                     :+++===:.::=-===+*%@===@@=
#                    .:#%-=--::.-=-=+#*+==-+=#@+
#                    .-#%@%+:::::+%#+##-=:.**-@+
#                    .@@@@@#:::.+@@@@@====.*#+**.
#                   ..=%%%*==::==*@@@@*:--:-*+%%:
#                   .=*+++++=++++++=++-==---+:#@@#=.
#                   .+******+-=******=::=*%%=.
#              ...::.:==-=+*+------=***-*@@@@%.::....
#          .-+*******-.-----:...:----=--+-::::-******+:
#              ..:-==+*+=-=+*****+===-::=***++==-:..
# ################################################################################

import os
import struct
import argparse

old_vs_new = {
    # Benny pos
    "993d1661":"6cff51b4",
    # Cyno posx
    "4cc92f60":"226f076e",
    # Fischl pos
    "9838aedf": "bf6aef4d",
    # Kirara pos
    "cc833025": "b57d7fe2",
    # Mona CN pos
    "ee5ed1dc": "515f3ce6",
    # Nahida all but draw
    "37ef15ec": "7106f05d",
    "bb58c686": "de60b92f",
    "f7b7ce48": "902b57ef",
    "b3f2e7da": "9b13c166",
    # Razor pos x
    "a099b935": "4662c505",
    # Xinyan pos
    "b3d31859": "76ed85f0",
    # CN Amber
    "7f94e8da": "557b2eff",

# These need remap --------------------------------------------------
    # Venti allx
    "d56e66b4": "0d36f587",
    "635466ca": "09a91a5c",
    "fd47c861": "a6823bb3",
    "bf8270d3": "6568ac68",
    "fbc0ffe1": "1afcf31d",
    # Mona Global pos and blendx
    "20d0bfab": "7a1dc890",
    "52f0e9a0": "b043715a",
    # Ning Base
    "6d197625": "4c2f9a0a",
    "55b43e99": "f9e1b52b",
    "9f7dc19c": "735eaea4",
    "906ad233": "1f0ab400",
    "abdc3768": "ad75352c",
    # Diluc Base all        
    "dff0b253": "5b0cb984",
    "6fdb0963": "71625c4d",
    "6fd20cc4": "afb527f6",
    "aee0755a": "6d0e22f0",
    "e9786c58": "e16fa548",
    # Xiao all
    "6f16afa7": "06c11756",
    "7f5ef8cc": "9464bf2d",
    "65a5e725": "258ab074",
    "ec61cc2b": "8ddd3ae9",
    "1df3eb2e": "ced409c1",
    # global Amber all but draw
    "caddc4c6": "a2ea4b2d",
    "ca5bd26e": "36d20a67",
    "e3047676": "81b777ca",
    "a1a2bbfb": "b03c7e30",
}

remaps = {"caddc4c6": ('Amber Global',[7,6,9,10,11,29,8,12,13,14,15,16,17,77,1,0,
                       73,18,19,20,21,53,70,74,50,30,47,51,76,75,24,
                       71,28,27,54,52,31,72,55,56,61,58,62,64,65,67,
                       68,57,59,60,63,66,69,48,26,25,49,32,33,38,35,
                       39,41,42,44,45,34,36,37,40,43,46,22,23,2,3,
                       4,5]),
          "52f0e9a0": ('Mona Global',[37, 38, 39, 36, 58, 30, 31, 32, 29, 57, 26,
                        25, 24, 27, 28, 34, 35, 40, 33, 81, 106, 102,
                        47, 43, 46, 44, 42, 41, 45, 105, 104, 60, 54,
                        53, 20, 83, 56, 55, 21, 15, 10, 16, 11, 5, 23,
                        0, 6, 1, 22, 77, 49, 50, 100, 51, 52, 79, 2, 7,
                        3, 4, 8, 9, 12, 17, 13, 14, 18, 19, 59, 76, 82,
                        99, 80, 103, 48, 101, 84, 90, 87, 93, 96, 97, 85,
                        86, 88, 89, 91, 92, 94, 95, 98, 78, 61, 67, 64, 70,
                        73, 74, 62, 63, 65, 66, 68, 69, 71, 72, 75,]),
          "6d197625": ('Ningguang Base',[70, 6, 20, 21, 22, 12, 13, 14, 15, 16, 7, 17,
                        18, 19, 8, 9, 10, 11, 4, 5, 69, 54, 53, 94, 111, 115, 71, 88,
                        92, 91, 52, 114, 116, 117, 118, 95, 93, 67, 72, 65, 68, 60, 61,
                        62, 63, 64, 66, 55, 56, 57, 58, 59, 40, 44, 45, 32, 23, 29, 24,
                        33, 37, 38, 30, 89, 90, 73, 79, 76, 82, 85, 86, 74, 75, 77, 78,
                        80, 81, 83, 84, 87, 2, 0, 112, 113, 96, 102, 99, 105, 108, 109,
                        97, 98, 100, 101, 103, 104, 106, 107, 110, 41, 43, 48, 28, 3,
                        1, 31, 36, 35, 34, 26, 27, 25, 39, 49, 51, 47, 46, 42, 50,]),
          "dff0b253": ('Diluc Base',[77, 78, 79, 57, 37, 4, 9, 6, 7, 8, 10, 5, 39, 32,
                        31, 53, 54, 49, 50, 51, 46, 47, 48, 43, 44, 45, 40, 41, 42, 80,
                        81, 82, 59, 34, 33, 73, 74, 69, 70, 71, 66, 67, 68, 63, 64, 65,
                        60, 61, 62, 83, 84, 85, 1, 3, 2, 0, 21, 22, 25, 26, 27, 13, 14,
                        15, 16, 28, 29, 30, 17, 18, 19, 20, 23, 24, 12, 55, 38, 52, 56,
                        75, 58, 72, 76, 35, 36, 11]),
          "6f16afa7": ('Xiao',[8, 47, 37, 7, 12, 13, 14, 10, 9, 11, 71, 48, 91, 38, 93,
                        68, 88, 92, 65, 69, 95, 72, 45, 49, 43, 70, 94, 44, 67, 66, 50,
                        56, 53, 59, 62, 63, 51, 52, 54, 55, 57, 58, 60, 61, 64, 39, 90,
                        89, 74, 73, 79, 76, 82, 85, 86, 75, 77, 78, 80, 81, 83, 84, 87,
                        40, 42, 41, 5, 36, 6, 33, 30, 29, 26, 25, 35, 34, 31, 32, 28, 27,
                        15, 16, 17, 18, 19, 21, 22, 23, 24, 20, 0, 1, 4, 3, 2, 46,]),
          "fd47c861": ('Venti',[114, 115, 116, 91, 68, 49, 50, 47, 48, 51, 52, 53, 54,
                        55, 56, 93, 110, 111, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103,
                        104, 105, 106, 107, 108, 65, 66, 39, 40, 43, 44, 25, 26, 27, 28,
                        29, 19, 24, 20, 21, 22, 23, 70, 87, 88, 71, 72, 73, 74, 75, 76, 77,
                        78, 79, 80, 81, 82, 83, 84, 85, 64, 63, 7, 8, 9, 10, 11, 41, 42, 37,
                        38, 1, 2, 3, 4, 5, 6, 46, 45, 12, 13, 14, 15, 16, 17, 18, 30, 31, 32,
                        33, 34, 35, 36, 0, 89, 69, 86, 90, 112, 92, 109, 113, 67, 57, 58, 59,
                        60, 61, 62,]),
        }

def process_folder(folder_path):
    '''Process all the files in the folder and subfolders,
    remapping the VG groups and replacing the old values with the new ones.'''
    for root, dirs, files in os.walk(folder_path):
        blend_files = [x for x in files if "blend" in x.lower() and ".buf" in x.lower()]
        for file in [x for x in files if x.lower().endswith('.ini') and x.lower() != 'desktop.ini']:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding="utf-8") as f:
                    s = f.read()
                    old_stream = s
                for x, vg_remap in remaps.items():
                    if x not in s:
                        continue
                    same_folder_blends = [blend_file for blend_file in blend_files
                        if os.path.dirname(os.path.join(root, blend_file)) == os.path.dirname(file_path)]
                    if len(same_folder_blends) == 0:
                        print(f'No blend file found for {vg_remap[0]} in file: {file_path}')
                        continue
                    print(f'Found blend for {vg_remap[0]}. Remapping...')
                    for blend_file in same_folder_blends:
                        with open(os.path.join(root, blend_file), "rb") as g:
                            blend_data = g.read()
                            remap_data = remap(blend_data, vg_remap[1])
                        with open(os.path.join(root, blend_file), "wb") as g:
                            g.write(remap_data)
                            print(f"File: {blend_file} VGs has been remapped succesfully!")
                        blend_files.remove(blend_file)
                        same_folder_blends.remove(blend_file)
                for old, new in old_vs_new.items():
                    s = s.replace(old, new)
                if s != old_stream:
                    print(f'File: {file_path} has been modified!')
                else:
                    print(f'File: {file_path} had no matches. Skipping')
                with open(file_path, 'w', encoding="utf-8") as f:
                    f.write(s)
            except Exception as e:
                print(f'Error processing file: {file_path}')
                print(e)
                continue

def force_remap(folder):
    '''Force remap a character based on the remap options.'''
    print('Remap options:')
    for i, (k,v) in enumerate(remaps.items()):
        print(f'{i+1}: {v[0]}')
    option = -1
    while option == -1:
        try:
            option = int(input('Select a character to remap: ')) - 1
            if option < 0 or option >= len(remaps):
                print('Invalid option')
                option = -1
        except ValueError:
            print('Invalid option')
            option = -1
        for i, (k,v) in enumerate(remaps.items()):
            if option == i:
                option = k
    for root, dirs, files in os.walk(folder):
        blend_files = [x for x in files if "blend" in x.lower() and ".buf" in x.lower()
                    and os.path.dirname(os.path.join(root, x)) == folder]
        if len(blend_files) == 0:
            print("No blend file found in this folder. Aborting!")
        for blend_file in blend_files:
            try:
                with open(os.path.join(root, blend_file), "rb") as g:
                    blend_data = g.read()
                    remap_data = remap(blend_data, remaps[option][1])
                with open(os.path.join(root, blend_file), "wb") as g:
                    g.write(remap_data)
                    print(f"File: {blend_file} VGs has been remapped succesfully!")
            except Exception as e:
                print(f'Error processing file: {blend_file}')
                print(e)
                continue

def remap(blend_data, vg_remap):
    '''Remap the VG groups in the blend file'''
    stride = 32
    remapped_blend = bytearray()
    if len(blend_data) % stride != 0:
        raise ValueError("Invalid blend file")
        # print("Invalid blend file. Making backup...")
    for i in range(0, len(blend_data), stride):
        # if i+stride > len(blend_data):
        #     continue
        blendweights = struct.unpack_from("<ffff", blend_data, i)
        blendindices = struct.unpack_from("<IIII", blend_data, i + 16)
        outputweights = bytearray()
        outputindices = bytearray()
        outputweights += struct.pack("<ffff", *blendweights)
        for x in range(4):
            if blendweights[x] != 0 and blendindices[x] in vg_remap:
                outputindices += struct.pack("<I", vg_remap[blendindices[x]])
            else:
                outputindices += struct.pack("<I", blendindices[x])
        remapped_blend += outputweights
        remapped_blend += outputindices
    if len(remapped_blend) % stride != 0:
        raise ValueError("Remapped blend file is invalid")
    return remapped_blend

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--force_remap', action='store_true',default=False)
    args = parser.parse_args()
    if args.force_remap:
        force_remap(os.getcwd())
    else:
        process_folder(os.getcwd())
    input('Done!')
