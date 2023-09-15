# Author: leotorrez
# Multiplies weights across the whole model evenly. Used to scale characters up. 

import os
import struct
import json

def main():

    print("\nWeight Multiplier(Character Scaler)\n")
    print("Guess what it does :3 \n")
    multiplier = float(input("Multiplier: "))

    # Generalized to all subdir so it works on merged mods
    for root, dirs, files in os.walk("."):
        blend_files = [file for file in files if os.path.splitext(file)[1] == ".buf" and "Blend.buf" in file]
        print(blend_files)
        blend_file = blend_files[0]
        print(f"Found {root}\\{blend_file}")

        with open(os.path.join(root, blend_file), "rb") as f:
            blend_data = f.read()

        if len(blend_data) % 32 != 0:
            print("ERROR: Blend file format not recognized")
            return

        multiplied_blend = multiply(blend_data, multiplier)

        # Finally, save results
        # No backups, we balling
        print("Saving results")

        with open(os.path.join(root, blend_file), "wb") as f:
            f.write(multiplied_blend)
            
    print("All operations complete, exiting")

def multiply(blend_data,multiplier):
    print("Beginning Remap")
    remapped_blend = bytearray()
    for i in range(0, len(blend_data), 32):
        blendweights = [struct.unpack("<f", blend_data[i + 4 * j:i + 4 * (j + 1)])[0] for j in range(4)]
        blendindices = [struct.unpack("<I", blend_data[i + 16 + 4 * j:i + 16 + 4 * (j + 1)])[0] for j in range(4)]
        outputweights = bytearray()
        outputindices = bytearray()
        for weight, index in zip(blendweights, blendindices):
            outputweights += struct.pack("<f", weight*multiplier)
            outputindices += struct.pack("<I", index)
        remapped_blend += outputweights
        remapped_blend += outputindices
    print("Remap Complete")
    return remapped_blend

if __name__ == "__main__":
    main()
