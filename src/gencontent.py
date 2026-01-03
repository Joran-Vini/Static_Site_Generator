import os
from to_html_node import markdown_to_html_node

def extract_title(markdown):
    header = markdown.split('\n')[0]
    if not header.startswith('# '):
        raise ValueError("No title found in markdown")
    return header[2:].strip()


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, item)
        if os.path.isdir(full_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(full_path, template_path, new_dest_dir, basepath)
        elif item.endswith('.md'):
            dest_file_path = os.path.join(dest_dir_path, item[:-3] + '.html')
            generate_page(full_path, template_path, dest_file_path, basepath)