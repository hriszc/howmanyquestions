#!/usr/bin/env python3
"""
HowManyQ Sitemap Generator
Generates XML sitemap for search engine optimization
"""

import json
import os
from datetime import datetime
from xml.dom.minidom import Document
from pathlib import Path

def generate_sitemap():
    """Generate XML sitemap for the HowManyQ site"""
    
    # Read navigation data
    nav_file = Path("navigation_data.json")
    if not nav_file.exists():
        print("❌ Error: navigation_data.json not found!")
        return None
    
    with open(nav_file, 'r', encoding='utf-8') as f:
        nav_data = json.load(f)
    
    # Create XML document
    doc = Document()
    
    # Root element
    urlset = doc.createElement("urlset")
    urlset.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    doc.appendChild(urlset)
    
    # Get current date for lastmod
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Add homepage
    home_url = doc.createElement("url")
    
    home_loc = doc.createElement("loc")
    home_loc_text = doc.createTextNode("https://howmanyq.com/")
    home_loc.appendChild(home_loc_text)
    home_url.appendChild(home_loc)
    
    home_lastmod = doc.createElement("lastmod")
    home_lastmod_text = doc.createTextNode(current_date)
    home_lastmod.appendChild(home_lastmod_text)
    home_url.appendChild(home_lastmod)
    
    home_changefreq = doc.createElement("changefreq")
    home_changefreq_text = doc.createTextNode("daily")
    home_changefreq.appendChild(home_changefreq_text)
    home_url.appendChild(home_changefreq)
    
    home_priority = doc.createElement("priority")
    home_priority_text = doc.createTextNode("1.0")
    home_priority.appendChild(home_priority_text)
    home_url.appendChild(home_priority)
    
    urlset.appendChild(home_url)
    
    # Add tool pages
    for tool in nav_data.get('tools', []):
        url = doc.createElement("url")
        
        # Location
        loc = doc.createElement("loc")
        # Clean the folder name to remove special Unicode characters
        folder_name = tool['folder_name']
        # Remove zero-width spaces and other invisible characters
        clean_folder_name = folder_name.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '').replace('\ufeff', '').strip()
        loc_text = doc.createTextNode(f"https://howmanyq.com/{clean_folder_name}/")
        loc.appendChild(loc_text)
        url.appendChild(loc)
        
        # Last modified
        lastmod = doc.createElement("lastmod")
        lastmod_text = doc.createTextNode(current_date)
        lastmod.appendChild(lastmod_text)
        url.appendChild(lastmod)
        
        # Change frequency
        changefreq = doc.createElement("changefreq")
        changefreq_text = doc.createTextNode("monthly")
        changefreq.appendChild(changefreq_text)
        url.appendChild(changefreq)
        
        # Priority
        priority = doc.createElement("priority")
        priority_text = doc.createTextNode("0.8")
        priority.appendChild(priority_text)
        url.appendChild(priority)
        
        urlset.appendChild(url)
    
    # Write to file
    sitemap_file = Path("sitemap.xml")
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        # Pretty print with indentation
        xml_str = doc.toprettyxml(indent="  ")
        # Remove extra blank lines
        xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])
        f.write(xml_str)
    
    return sitemap_file, len(nav_data.get('tools', []))

def main():
    """Main function"""
    print("🔍 HowManyQ Sitemap Generator")
    print("=" * 50)
    
    result = generate_sitemap()
    
    if result:
        sitemap_file, tool_count = result
        print(f"✅ Sitemap generated successfully!")
        print(f"📁 Output file: {sitemap_file}")
        print(f"🔢 Total URLs: {tool_count + 1} (1 homepage + {tool_count} tools)")
        print()
        print("📋 Sitemap Details:")
        print("- Homepage: https://howmanyq.com/ (priority: 1.0, changefreq: daily)")
        print(f"- Tool pages: {tool_count} pages (priority: 0.8, changefreq: monthly)")
        print()
        print("📝 Next steps:")
        print("1. Submit sitemap.xml to Google Search Console")
        print("2. Submit sitemap.xml to Bing Webmaster Tools")
        print("3. Add sitemap URL to robots.txt")

if __name__ == "__main__":
    main()
