import os

folder_path = os.getcwd() # gets the current working directory

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isdir(file_path):
            process_folder(file_path)
        elif filename.endswith('.ini'):
            with open(file_path, 'r') as f:
                s = f.read()
            s = s.replace('75e78f78', '37c70461')
            s = s.replace('531b64bc', '5db2f8f4')
            s = s.replace('3e6a5d39', 'd77ffc4f')
            with open(file_path, 'w') as f:
                f.write(s)

process_folder(folder_path)
print('done')