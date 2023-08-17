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
            s = s.replace('7d8a4e0f', '2a557add')
            s = s.replace('de1311ae', '8bfa989d')
            s = s.replace('50ae5602', '92b87c71')
            with open(file_path, 'w') as f:
                f.write(s)

process_folder(folder_path)
print('done')