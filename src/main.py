import os
import shutil
from textnode import TextNode
from generate_page import *


def main():
    dir_or = "./static"
    dir_dest = "./public"
    recursive_copy(dir_or, dir_dest)

    generate_pages_recursive("content", "template.html", "public")


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