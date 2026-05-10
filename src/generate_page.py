import os
from markdown_handling import markdown_to_html_node
from extract_title import *
from pathlib import Path

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        from_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    html_string = markdown_to_html_node(from_content).to_html()
    html_title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", html_title)
    template_content = template_content.replace("{{ Content }}", html_string)

    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    dir_paths = os.path.dirname(dest_path)

    if dir_paths:
        os.makedirs(dir_paths, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content = os.listdir(dir_path_content)

    for item in content:   
        source_path = os.path.join(dir_path_content, item)    
        dest_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(source_path):
            if item.endswith(".md"):
                if not os.path.exists(dest_dir_path):
                    os.makedirs(dest_dir_path)

                file_name = os.path.splitext(item)[0]
                output_path = os.path.join(dest_dir_path, f"{file_name}.html")

                generate_page(source_path, template_path, output_path, basepath)
                
        elif os.path.isdir(source_path):
            generate_pages_recursive(source_path, template_path, dest_path, basepath)