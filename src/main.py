import os
import shutil
import sys
from textnode import TextNode
from generate_page import *


def main():
    
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    dir_or = "./static"
    dir_dest = "./docs"
    if not os.path.exists(dir_dest):
        os.mkdir(dir_dest)

    recursive_copy(dir_or, dir_dest)

    generate_pages_recursive("content", "template.html", "docs", basepath)


def recursive_copy(source, destination, first_call=True):
    # clear the destination and create a new one
    if first_call:
        if os.path.exists(destination): 
            print(f"Cleaning destination: {destination}")
            shutil.rmtree(destination)
            os.mkdir(destination)

    # start copying files
    if os.path.exists(source):
        items = os.listdir(source)

        for item in items:
            source_path = os.path.join(source, item)
            dest_path = os.path.join(destination, item)

            if os.path.isfile(source_path):
                print(f"Copying file: {source_path} - > {dest_path}")
                shutil.copy(source_path, dest_path)
            else:
                print(f"Entering directory: {source_path}")
                os.mkdir(dest_path)
                recursive_copy(source_path, dest_path, first_call=False)


if __name__ == "__main__":
    main()