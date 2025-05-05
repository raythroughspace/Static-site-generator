from textnode import *
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
)
from website import *
import os
import shutil

# delete all files from dst and copy all files from src to dst
def delete_and_copy(src, dst):
    shutil.rmtree(dst)
    os.mkdir(dst)
    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)

        if (os.path.isfile(src_path)):
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            delete_and_copy(src_path, dst_path)


def main():
    delete_and_copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    

if __name__ == "__main__":
    main()