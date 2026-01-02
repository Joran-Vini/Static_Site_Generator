import os
import shutil

from textnode import TextNode, TextType
from to_html_node import markdown_to_html_node

def main():
    recursive_static_to_public()
    generate_page('content/index.md', 'template.html', 'public/index.html')

def recursive_static_to_public():
    source_dir = 'static'
    target_dir = 'public'

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    

    copy_directory(source_dir, target_dir)

def copy_directory(source, target):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        t = os.path.join(target, item)

        if os.path.isdir(s):
            os.makedirs(t, exist_ok=True)
            copy_directory(s, t)
        else:
            shutil.copy2(s, t)


def extract_title(markdown):
    header = markdown.split('\n')[0]
    if not header.startswith('# '):
        raise ValueError("No title found in markdown")
    return header[2:].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    with open(dest_path, 'w') as f:
        f.write(final_html)

if __name__ == "__main__":
    main()