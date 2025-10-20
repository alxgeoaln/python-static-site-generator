import os
import shutil

PUBLIC_PATH = "./public"
STATIC_PATH = "./static"

def copy_static():
    public_folder_exists = os.path.exists(PUBLIC_PATH)
    if public_folder_exists:
        shutil.rmtree(PUBLIC_PATH)
        os.mkdir(PUBLIC_PATH)
    else:
        os.mkdir(PUBLIC_PATH)
    
    def copy(path, destination):
        contents = os.listdir(path)
        
        for content in contents:
            new_path = f"{path}/{content}"
            new_destination = f"{destination}/{content}"
            if os.path.isfile(new_path):
                shutil.copy(new_path, f"{new_destination}")
                continue
            
            os.mkdir(new_destination)
            copy(new_path, new_destination)
    
    copy(STATIC_PATH, PUBLIC_PATH)
        