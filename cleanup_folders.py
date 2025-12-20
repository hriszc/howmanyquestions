import os
import shutil
import re

def clean_name(name):
    # Remove zero-width spaces and other non-printable characters
    cleaned = re.sub(r'[^\x20-\x7E]', '', name)
    # Replace spaces with underscores or keep as is? 
    # The sitemap uses spaces in some places and underscores in others.
    # Let's be consistent. Standard SEO practice is hyphens or underscores.
    # But looking at sitemap.xml, it uses spaces: "how many calories should i eat a day/"
    # Wait, sitemap.xml actually has spaces in <loc>. This is unusual but possible.
    # However, many folders use underscores.
    
    # Let's just strip the invisible characters first.
    return cleaned.strip()

def rename_folders():
    for root, dirs, files in os.walk('.', topdown=True):
        for d in dirs:
            new_name = clean_name(d)
            if new_name != d:
                old_path = os.path.join(root, d)
                new_path = os.path.join(root, new_name)
                print(f"Renaming: '{d}' -> '{new_name}'")
                if os.path.exists(new_path):
                    print(f"Warning: {new_path} already exists. Merging content...")
                    # Merge content if necessary, or just skip
                    for item in os.listdir(old_path):
                        s = os.path.join(old_path, item)
                        d_item = os.path.join(new_path, item)
                        if os.path.isdir(s):
                            shutil.copytree(s, d_item, dirs_exist_ok=True)
                        else:
                            shutil.copy2(s, d_item)
                    shutil.rmtree(old_path)
                else:
                    os.rename(old_path, new_path)
        # Only do top level for now to avoid confusion
        break 

if __name__ == "__main__":
    rename_folders()
