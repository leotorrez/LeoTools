import os
import argparse
import re
import struct
import sys

def main():
    '''Generates a merged mod from several mod folders'''
    parser = argparse.ArgumentParser(description="Generates a merged mod from several mod folders")
    parser.add_argument("-r", "--root", type=str,  default=".", help="Location to use to create mod")
    parser.add_argument("-s", "--store", action="store_true", help="Use to keep the original mod folders after completion")
    parser.add_argument("-d", "--destination", type=str, default="", help="Location to use to create mod")
    parser.add_argument("-k", "--keys", type=str, nargs='*', default= ["ctrl VK_NUMPAD0","ctrl VK_NUMPAD1","ctrl VK_NUMPAD2","ctrl VK_NUMPAD3","ctrl VK_NUMPAD4","ctrl VK_NUMPAD5","ctrl VK_NUMPAD6","ctrl VK_NUMPAD7","ctrl VK_NUMPAD8","ctrl VK_NUMPAD9"], help="Keys to use for the merged mod")
    parser.add_argument("-p", "--parts", type=str, nargs='*', default= ["Head", "Body", "Dress", "Extra", "Extra2", "Extra3", "Extra4"], help="Parts to use for the merged mod. In the case of HSR ABCD... is recommended")
    parser.add_argument("-c", "--components", type=str, nargs='*', default= [], help="Components to use for the merged mod, it will be used as the variable names in the ini.")
    parser.add_argument("--modparts", type=str, nargs='*', default= [""], help="Parts for mods with several components. ORDER IS CRUCIAL!!!- Must be the same order as in the exported inis. Ex: \"Hair\", \"Body\", \"Face\" for HSR\", for genshin: \"\",\"Face\" ") 
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.1")
    args = parser.parse_args()
    if args.destination == "":
        args.destination = os.path.join(args.root, "Result")

    if not args.store:
        print("This script will merge all the mods in the specified folder and delete the original files. Make sure to have a backup or use -s(--store) to skip the cleaning step.")
        print(f"Destination: {args.destination}")
        input("Press Enter to continue.")

    counts = {}
    for k, modpart in enumerate(args.modparts):
        mod_data, mod_name, first_ini_path = process_folders(args.root, args.destination, args.parts, modpart)
        if len(mod_data.keys()) == 0 and k==0:
            print(f"Error: No mod folders found in {args.root}.")
            input("Press ENTER to exit.")
            sys.exit()

        if (len(mod_data.keys()) > len(args.keys) or (args.components != [] and len(mod_data.keys()) > len(args.components))) and k==0:
            print("Error: The number of parts and keys must be the same or more as the number of mods to merge.")
            print(f"Keys: {args.keys}")
            print(f"Mods: {len(mod_data.keys())}")
            print(f"Components: {args.components}")
            input("Press ENTER to exit.")
            sys.exit()

        if not os.path.exists(args.destination) and k==0:
            os.mkdir(args.destination)

        counts[modpart] = (merge_buffers(mod_data, args.root, mod_name, args.destination, args.parts, modpart))

    with (open(first_ini_path, 'r', encoding='utf-8') as input_file,
        open(os.path.join(args.destination, mod_name+'.ini'), 'w',encoding='utf-8') as output_file):
        ini_data = input_file.read()
        output_file.write(generate_ini(ini_data, counts, args.keys, args.components, args.modparts))

    copy_textures(args.root, mod_data, args.destination)

    if not args.store:
        for folder in mod_data:
            recursive_delete(os.path.join(args.root,folder))

    print(f"Done! Merged mod is located at {os.path.join(args.root,mod_name+'.ini')}")

def process_folders(root:str, destination:str, labels:list[str], modpart:str):
    '''Processes the folders in the root directory and returns a dictionary with the mod data and the mod name.
    Also returns the path of the first ini file found in the root directory.'''
    files = [f for f in os.listdir(root) if f != destination if not f.lower().startswith('disabled')]
    folders = [f for f in files if os.path.isdir(os.path.join(root,f))]
    mod_data = {}
    mod_name = ''
    first_ini_path = ''
    labels = [f"{modpart}{l}" for l in labels]
    for folder in folders:
        if os.path.join(root,folder) == destination:
            continue
        mod_data[folder] = {'ibs': [], 'vbs': {'pos':'','tex':'','blend':''}}
        for f in os.listdir(os.path.join(root,folder)):
            if os.path.isfile(os.path.join(root,folder,f)):
                if f.lower().endswith('.ib') and modpart.lower() in f[len(mod_name):-3].lower():
                    mod_data[folder]['ibs'].append(f)
                elif f.lower().endswith('.buf') and modpart.lower() in f[len(mod_name):-4].lower():
                    if 'position.buf' in f.lower():
                        mod_data[folder]['vbs']['pos'] = f
                    elif 'blend.buf' in f.lower() and modpart.lower() in f[len(mod_name):-4].lower():
                        mod_data[folder]['vbs']['blend'] = f
                    elif 'texcoord.buf' in f.lower() and modpart.lower() in f[len(mod_name):-4].lower():
                        mod_data[folder]['vbs']['tex'] = f
            if mod_name == '' and f.endswith('.ini'):
                mod_name = f[:-4]
                first_ini_path = os.path.join(root,folder,f)
        mod_data[folder]['ibs'] = sorted(mod_data[folder]['ibs'], key=lambda x: labels.index(x[len(mod_name):-3]))

    return mod_data, mod_name, first_ini_path

def merge_buffers(mod_data:dict, root:str, mod_name:str, destination:str, labels:list[str], modpart:str):
    '''Merges the buffers of the mod data and returns the counts of the merged buffers.'''
    counts = {'parts': len(mod_data[list(mod_data.keys())[0]]['ibs']),'vertex': 0,'mods': len(mod_data),'idx_counts':[]}
    pos_data = bytearray()
    tex_data = bytearray()
    blend_data = bytearray()
    for i in range(counts['parts']):
        ib_data =  bytearray()
        ib_offset = 0
        counts['idx_counts'].append([])
        for j, fol in enumerate(mod_data):
            with (open(os.path.join(root,fol, mod_data[fol]['ibs'][i]), "rb") as ib,
                open(os.path.join(root,fol, mod_data[fol]['vbs']['pos']), "rb") as p):
                while True:
                    a = ib.read(4) # DXGI_FORMAT_R32_UINT
                    if not a:
                        break
                    a = struct.unpack('I', a)
                    ib_data += struct.pack('I', a[0] + ib_offset)
                ib_offset += int(len(p.read())/40)
                ib.seek(0)
                counts['idx_counts'][i].append(int(len(ib.read())/4))
        try:
            path = os.path.join(destination,f"{mod_name}{modpart}{labels[i]}.ib")
            with open(path, "wb") as f:
                f.write(ib_data)
                print(f"merged ib {i} with {len(ib_data.splitlines())} lines")
                print(f"Path: {path}")
        except IndexError:
            pass

    for i in range(counts['mods']):
        with (open(os.path.join(root, list(mod_data.keys())[i], mod_data[list(mod_data.keys())[i]]['vbs']['pos']), "rb") as p,
            open(os.path.join(root, list(mod_data.keys())[i], mod_data[list(mod_data.keys())[i]]['vbs']['blend']), "rb") as b,
            open(os.path.join(root, list(mod_data.keys())[i], mod_data[list(mod_data.keys())[i]]['vbs']['tex']), "rb") as t):
            pos_data += p.read()
            tex_data += t.read()
            blend_data += b.read()

    with (open(os.path.join(destination, f"{mod_name}{modpart}Position.buf"), "wb") as p,
        open(os.path.join(destination, f"{mod_name}{modpart}Texcoord.buf"), "wb") as t,
        open(os.path.join(destination, f"{mod_name}{modpart}Blend.buf"), "wb") as b):
        p.write(pos_data)
        t.write(tex_data)
        b.write(blend_data)
        print(f"merged position with {len(pos_data.splitlines())} lines")
        print("Path:", os.path.join(destination,f"{mod_name}{modpart}Position.buf"))
        print(f"merged texcoord with {len(tex_data.splitlines())} lines")
        print("Path:", os.path.join(destination,f"{mod_name}{modpart}Texcoord.buf"))
        print(f"merged blend with {len(blend_data.splitlines())} lines")
        print("Path:", os.path.join(destination,f"{mod_name}{modpart}Blend.buf"))
        
    counts['vertex'] = int(len(pos_data)/40)
    return counts

def generate_ini(ini_data:dict, counts:dict, keys:list[str], variables:list[str], modparts:list[str]):
    '''Generates the merged ini file from the original ini file and the counts of the merged buffers.'''
    ini_data = ini_data.replace('drawindexed = auto', '')
    primerapart = True
    loops = []
    keyswaps = ""
    definitions = "[Constants]\n"
    search_draws = re.findall(r'draw = \d+,0', ini_data, re.DOTALL)
    for modpart in modparts:
        drawcount = f"draw = {counts[modpart]['vertex']}, 0"
        if variables == []:
            variables = [f"variable{i}" for i in range(len(counts[modpart]['idx_counts'][0]))]
        for part in counts[modpart]['idx_counts']:
            loop = ""
            offset = 0
            i = 0
            for num in part:
                if primerapart:
                    definitions += f"global persist ${variables[i]} = 0\n"
                    keyswaps += f"""[KeySwap{i}]
key = {keys[i]}
condition = $active == 1
type = cycle
${variables[i]} = 0,1
"""
                loop += f"if ${variables[i]} == 1\n  drawindexed = {num}, {offset}, 0\nendif\n"
                offset += num
                i += 1
            primerapart = False
            loops.append(loop)
        ini_data = ini_data.replace(search_draws.pop(0), drawcount)
    # TODO: 3.0 charas with not normals on all parts will move the texture slot later down the ini
    search = re.findall(r'ps-t2 = \w+', ini_data, re.DOTALL)
    if len(search) != len(loops):
        search = re.findall(r'ps-t1 = \w+', ini_data, re.DOTALL)
    if len(search) != len(loops):
        search = re.findall(r'ib = \w+', ini_data, re.DOTALL)
    for s in search:
        try:
            ini_data = ini_data.replace(s, f"{s}\n{loops.pop(0)}")
        except IndexError:
            print("Error: Loop count does not match the number of parts.")
            input("Press ENTER to continue.")

    ini_data = re.sub(r'\Z', f'\n{definitions}{keyswaps}\n', ini_data)
    return ini_data

def copy_textures(root, mod_data, destination):
    '''Copies the textures from the mod data to the destination folder.'''
    fol = list(mod_data.keys())[0]
    files = [f for f in os.listdir(os.path.join(root,fol))
            if not f.lower().endswith('.ib')
            and not f.lower().endswith('.buf')
            and not f.lower().endswith('.ini') ]
    i = 0
    for f in files:
        print(f"Moving {f} to {os.path.join(destination,f)} ({i}/{len(files)})")
        i += 1
        with (open(os.path.join(root,fol,f), "rb") as src,
            open(os.path.join(destination,f), "wb") as dest):
            dest.write(src.read())
        print(f"Moved {f} to {os.path.join(destination,f)} ({i}/{len(files)})")

def recursive_delete(path):
    '''Deletes the specified path and its contents.'''
    if os.path.isdir(path):
        for f in os.listdir(path):
            recursive_delete(os.path.join(path,f))
        os.rmdir(path)
    else:
        os.remove(path)
if __name__ == "__main__":
    main()
