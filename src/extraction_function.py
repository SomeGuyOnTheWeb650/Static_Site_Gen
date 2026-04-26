import os
from markdown_blocks import markdown_to_blocks, BlockType, block_to_blocktype
from markdown_to_html import markdown_to_html_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_blocktype(block) == BlockType.HEADING:
            h1 = "# "
            if block.startswith(h1):
                result = block.strip("# ")
                return result
    raise Exception("no h1 heading found!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:

        src = f.read()
    with open(template_path) as f:

        template = f.read()
    html_string = markdown_to_html_node(src).to_html()
    title = extract_title(src)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    
    if not os.path.exists(dest_path):
        dirpath = os.path.dirname(dest_path)
        os.makedirs(dirpath, exist_ok=True)
    
    
    with open(dest_path, "w") as f:
        f.write(template)

    
