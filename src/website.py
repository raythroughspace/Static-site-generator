import os
from block_markdown import *

def extract_title(markdown):
    first_block = markdown_to_blocks(markdown)[0]
    block_type = block_to_block_type(first_block)
    if (block_type != BlockType.HEADING):
        raise Exception("Title must be a heading block type")
    if (len(re.findall(r"(#+)", first_block)[0]) != 1):
        raise Exception("Title must be a h1 header")
    return first_block.strip("#").strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    
    with open(template_path) as f:
        template = f.read()

    page_html = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template.replace("{{ Title }}", page_title).replace("{{ Content }}", page_html))

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dst_path = os.path.join(dest_dir_path, entry.replace(".md", ".html"))
        if (os.path.isfile(src_path)):
            generate_page(src_path, template_path, dst_path)
        else:
            generate_pages_recursive(src_path, template_path, dst_path)
