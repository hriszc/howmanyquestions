import os
import re
from pathlib import Path

def enhance_html(file_path, folder_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Canonical Tag
    base_url = "https://howmanyq.com/"
    canonical_url = f"{base_url}{folder_name}/"
    canonical_tag = f'<link rel="canonical" href="{canonical_url}" />'
    
    if 'rel="canonical"' not in content:
        content = re.sub(r'(</title>)', r'\1\n  ' + canonical_tag, content)
    else:
        # Update existing canonical if needed
        content = re.sub(r'<link rel="canonical" href="[^\"]*" />', canonical_tag, content)

    # 2. Hreflang Tags
    hreflang_tags = f'''
    <link rel="alternate" hreflang="en" href="{canonical_url}" />
    <link rel="alternate" hreflang="zh-CN" href="{canonical_url}?lang=zh" />
    <link rel="alternate" hreflang="x-default" href="{canonical_url}" />'''
    
    if 'hreflang=' not in content:
        content = re.sub(r'(</title>)', r'\1' + hreflang_tags, content)

    # 3. Add Header / Navigation Link (if missing)
    # Most pages use a container like <div class="app-shell"> or <body>
    header_html = '''
    <nav style="position: fixed; top: 0; left: 0; right: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); z-index: 1000; border-bottom: 1px solid #333; padding: 10px 20px;">
        <a href="/" style="color: white; text-decoration: none; font-family: sans-serif; font-weight: bold; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 20px;">🧮</span> HowManyQ Home
        </a>
    </nav>
    <div style="margin-top: 60px;"></div>
    '''
    
    # Check if a link to home already exists
    if 'href="/"' not in content and 'href=".."' not in content and 'HowManyQ Home' not in content:
        # Insert after <body>
        content = re.sub(r'(<body[^>]*>)', r'\1' + header_html, content)

    # 4. Ensure lang="en"
    if '<html lang="en">' not in content and '<html' in content:
        content = re.sub(r'<html([^>]*)>', r'<html lang="en"\1>', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_all_tools():
    for root, dirs, files in os.walk('.'):
        if 'index.html' in files and root != '.':
            folder_name = os.path.basename(root)
            file_path = os.path.join(root, 'index.html')
            print(f"Enhancing SEO for: {file_path}")
            enhance_html(file_path, folder_name)

if __name__ == "__main__":
    process_all_tools()
