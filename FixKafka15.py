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
            s = s.replace('deb266a8', '51abd7c9')
            s = s.replace('38072744', '17cb3b3e')
            s = s.replace('a6813fd5', '190e483a')
            s = s.replace('6d45dac8', 'e25c6ba9')
            s = s.replace('b7401039', '8d847042')
            with open(file_path, 'w') as f:
                f.write(s)

process_folder(folder_path)
print('done')