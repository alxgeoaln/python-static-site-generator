import os
import shutil

from .block_parser import markdown_to_html_node

PUBLIC_PATH = "./docs"
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
    
def extract_title(md_content):
    splitted = md_content.split("\n\n")
    print("splitted", splitted)
        
    for item in splitted:
        if item.startswith("#"):
            return item.split("#")[1]
    
def generate_page(from_path, template_path, dest_path, basepath="/"):
    md_content = None
    template_content = None
    
    with open(from_path, "r") as f:
        md_content = f.read()
        f.close()
        
    with open(template_path, "r") as f:
        template_content = f.read()
        f.close()
        
    content = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    
    html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content)
    
    # Replace path references with basepath
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')
    
    print("dest_pathdest_path", dest_path)
    print("from_pathfrom_path", from_path)
    with open(dest_path, "x") as f:
        f.write(html)
        f.close()
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    print("dest_dir_path::::", dest_dir_path)
    contents = os.listdir(dir_path_content)
    
    for content in contents:
        new_path_content = f"{dir_path_content}/{content}"
        new_path_dest = f"{dest_dir_path}/{content}"
        
        if os.path.isfile(new_path_content):
            file_name = os.path.splitext(os.path.basename(new_path_content))[0]
            generate_page(new_path_content, template_path, f"{dest_dir_path}/{file_name}.html", basepath)
            continue
        
        os.mkdir(new_path_dest)
        generate_pages_recursive(new_path_content, template_path, new_path_dest, basepath)
        
    
    
        
    
        