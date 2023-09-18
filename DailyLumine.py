# v 1.1
import os
import random

#configuration variables. 
path3dm="D:/Scripts/3dmigotoGenshin/Mods/"
gamepath = "C:/Program Files/Genshin Impact/Genshin Impact Game/GenshinImpact.exe"

#the name of the character refers to the folder within /Mods in your 3dmigotoGenshin folder.
#for example, lumine would equal to D:/Scripts/3dmigotoGenshin/Mods/Lumine
characterlist = [
    "Lumine",
    "Shenhe",
    "NPC/Katherine",
    "UI Stuff/Cursor",
    "Sucrose",
    "Yelan",
    "Noelle",
    "Barbara/Barbara Summer Skin",
    "Xiangling",
    "Dehya",
    "Lisa/LisaStudentSkin",
    "Lisa/LisaDefault",
    "Eula",
    "Lynette/Body",
    "Paimon",
]

def randomizeOutfit(character):
    directory_path = path3dm + character
    folders = [
        f
        for f in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, f)) and f.startswith("DISABLED")
    ]

    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.isdir(folder_path) and not folder_name.startswith("DISABLED"):
            new_folder_name = "DISABLED" + folder_name
            new_folder_path = os.path.join(directory_path, new_folder_name)
            os.rename(folder_path, new_folder_path)
            folders.append(new_folder_name)

    if folders:
        folder_to_rename = random.choice(folders)
        new_folder_name = folder_to_rename.replace("DISABLED", "", 1)
        folder_to_rename_path = os.path.join(directory_path, folder_to_rename)
        new_folder_path = os.path.join(directory_path, new_folder_name)
        os.rename(folder_to_rename_path, new_folder_path)
        print(f"Outfit Chosen: ", new_folder_name)

if __name__ == "__main__":
    try:
        for character in characterlist:
            randomizeOutfit(character)
    except Exception as e:
        print(f"An error occurred, randomization skiped. Error: {e}")
    finally:
        os.startfile(gamepath)
        print("Execution complete")
