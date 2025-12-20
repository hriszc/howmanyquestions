import os
import shutil
import re

def slugify(name):
    # Convert spaces and other chars to underscores
    slug = name.replace(' ', '_').strip('_')
    # Remove invisible characters
    slug = re.sub(r'[^\x20-\x7E]', '', slug)
    return slug

def merge_folders():
    # Get all items in current directory
    items = [d for d in os.listdir('.') if os.path.isdir(d)]
    
    for d in items:
        if d.startswith('.') or d in ['__pycache__', 'node_modules']:
            continue
            
        slug = slugify(d)
        if slug != d:
            old_path = d
            new_path = slug
            print(f"Merging: '{old_path}' -> '{new_path}'")
            
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
            else:
                # Merge contents
                for item in os.listdir(old_path):
                    s = os.path.join(old_path, item)
                    d_item = os.path.join(new_path, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d_item, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d_item)
                shutil.rmtree(old_path)

if __name__ == "__main__":
    merge_folders()
