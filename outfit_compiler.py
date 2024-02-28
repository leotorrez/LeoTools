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
    args = parser.parse_args()
    if args.destination == "":
        args.destination = os.path.join(args.root, "Result")

    if not args.store:
        print("This script will merge all the mods in the specified folder and delete the original files. Make sure to have a backup or use -s(--store) to skip the cleaning step.")
        print(f"Destination: {args.destination}")
        input("Press Enter to continue.")

    mod_data, mod_name, first_ini_path = process_folders(args.root, args.destination, args.parts)

    if len(mod_data.keys()) == 0:
        print(f"Error: No mod folders found in {args.root}.")
        input("Press ENTER to exit.")
        sys.exit()
        
    if len(mod_data.keys()) > len(args.keys) or (args.components != [] and len(mod_data.keys()) > len(args.components)):
        print("Error: The number of parts and keys must be the same or more as the number of mods to merge.")
        print(f"Keys: {args.keys}")
        print(f"Mods: {len(mod_data.keys())}")
        print(f"Components: {args.components}")
        input("Press ENTER to exit.")
        sys.exit()

    if not os.path.exists(args.destination):
        os.mkdir(args.destination)

    counts = merge_buffers(mod_data, args.root, mod_name, args.destination, args.parts)

    copy_textures(args.root, mod_data, args.destination)

    with (open(first_ini_path, 'r', encoding='utf-8') as input_file,
        open(os.path.join(args.destination, mod_name+'.ini'), 'w',encoding='utf-8') as output_file):
        ini_data = input_file.read()
        output_file.write(generate_ini(ini_data, counts, args.keys, args.components))

    if not args.store:
        for folder in mod_data:
            recursive_delete(os.path.join(args.root,folder))

    print(f"Done! Merged mod is located at {os.path.join(args.root,mod_name+'.ini')}")

def process_folders(root, destination, labels):
    '''Processes the folders in the root directory and returns a dictionary with the mod data and the mod name.
    Also returns the path of the first ini file found in the root directory.'''
    files = [f for f in os.listdir(root) if f != destination if not f.lower().startswith('disabled')]
    folders = [f for f in files if os.path.isdir(os.path.join(root,f))]
    mod_data = {}
    mod_name = ''
    first_ini_path = ''
    for folder in folders:
        mod_data[folder] = {'ibs': [], 'vbs': {'pos':'','tex':'','blend':''}}
        for f in os.listdir(os.path.join(root,folder)):
            if os.path.isfile(os.path.join(root,folder,f)):
                if f.lower().endswith('.ib'):
                    mod_data[folder]['ibs'].append(f)
                elif f.lower().endswith('.buf'):
                    if 'position.buf' in f.lower():
                        mod_data[folder]['vbs']['pos'] = f
                    elif 'blend.buf' in f.lower():
                        mod_data[folder]['vbs']['blend'] = f
                    elif 'texcoord.buf' in f.lower():
                        mod_data[folder]['vbs']['tex'] = f
            if mod_name == '' and f.endswith('.ini'):
                mod_name = f[:-4]
                first_ini_path = os.path.join(root,folder,f)
        mod_data[folder]['ibs'] = sorted(mod_data[folder]['ibs'], key=lambda x: labels.index(x[len(mod_name):-3]))

    return mod_data, mod_name, first_ini_path

def merge_buffers(mod_data, root, mod_name, destination, labels):
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
        
        path = os.path.join(destination,f"{mod_name}{labels[i]}.ib")
        with open(path, "wb") as f:
            f.write(ib_data)
            print(f"merged ib {i}")
            print(f"Path: {path}")

    for i in range(counts['mods']):
        with (open(os.path.join(root,list(mod_data.keys())[i], mod_data[list(mod_data.keys())[i]]['vbs']['pos']), "rb") as p,
            open(os.path.join(root,list(mod_data.keys())[i], mod_data[list(mod_data.keys())[i]]['vbs']['blend']), "rb") as b,
            open(os.path.join(root,list(mod_data.keys())[i], mod_data[list(mod_data.keys())[i]]['vbs']['tex']), "rb") as t):
            pos_data += p.read()
            tex_data += t.read()
            blend_data += b.read()

    with (open(os.path.join(destination, f"{mod_name}Position.buf"), "wb") as p,
        open(os.path.join(destination, f"{mod_name}Texcoord.buf"), "wb") as t,
        open(os.path.join(destination, f"{mod_name}Blend.buf"), "wb") as b):
        p.write(pos_data)
        t.write(tex_data)
        b.write(blend_data)
        print(f"merged position with {len(pos_data.splitlines())} lines")
        print("Path:", os.path.join(destination,f"{mod_name}Position.buf"))
        print(f"merged texcoord with {len(tex_data.splitlines())} lines")
        print("Path:", os.path.join(destination,f"{mod_name}Texcoord.buf"))
        print(f"merged blend with {len(blend_data.splitlines())} lines")
        print("Path:", os.path.join(destination,f"{mod_name}Blend.buf"))
        
    counts['vertex'] = int(len(pos_data)/40)
    return counts

def generate_ini(ini_data, counts, keys, variables):
    '''Generates the merged ini file from the original ini file and the counts of the merged buffers.'''
    loops = []
    drawcount = f"draw = {counts['vertex']}, 0"
    keyswaps = ""
    definitions = ""
    if variables == []:
        variables = [f"variable{i}" for i in range(len(counts['idx_counts'][0]))]
    primerapart = True
    for part in counts['idx_counts']:
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

    ini_data = re.sub(r'\[Present\]', f"{definitions}{keyswaps}\n[Present]", ini_data)
    ini_data = ini_data.replace('drawindexed = auto', '')
    search = re.findall(r'ps-t2 = \w+', ini_data, re.DOTALL)
    if len(search) != len(loops):
        search = re.findall(r'ps-t1 = \w+', ini_data, re.DOTALL)
    for s in search:
        ini_data = ini_data.replace(s, f"{s}\n{loops.pop(0)}")
    ini_data = re.sub(r'draw = \d+,0', drawcount, ini_data)
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
