#!/usr/bin/env python3
"""
HowManyQ Navigation Page Dynamic Discovery Tool
This script scans the directory structure to find all folders containing index.html files
and generates dynamic data for the navigation page.
"""

import os
import json
import re
from pathlib import Path
from urllib.parse import quote

class NavigationGenerator:
    def __init__(self, base_path="/Users/zhaochen/Desktop/2025/11/v2/howmanyq"):
        self.base_path = Path(base_path)
        self.excluded_folders = {
            '.DS_Store', '导航首页开发计划.md', '高级灰设计改造计划.md', 
            'create_folders.py', 'navigation_development_plan.md', 
            'questions.md', 'todo.md', 'todo_list.md'
        }
        
        # Category mapping for better organization
        self.category_mapping = {
            'time': ['christmas', 'days', 'weeks', 'months', 'hours', 'minutes', 'seconds'],
            'volume': ['ounces', 'cups', 'gallons', 'liters', 'pints', 'quarts', 'ml', 'tbsp', 'tsp'],
            'weight': ['pounds', 'ounces', 'grams', 'kilograms', 'tons', 'calories'],
            'length': ['feet', 'inches', 'meters', 'miles', 'yards', 'centimeters', 'millimeters'],
            'measurement': ['steps', 'bmi', 'temperature', 'fitness']
        }
        
        self.icon_mapping = {
            'time': '⏰',
            'volume': '🧪', 
            'weight': '⚖️',
            'length': '📏',
            'measurement': '📊',
            'calculator': '🧮',
            'countdown': '⏳',
            'conversions': '🔄'
        }
    
    def extract_keywords_from_folder(self, folder_name):
        """Extract meaningful keywords from folder name for categorization"""
        keywords = folder_name.lower().replace('_', ' ').replace('-', ' ').split()
        return keywords
    
    def determine_category(self, folder_name, keywords):
        """Determine the most appropriate category for a tool"""
        category_scores = {}
        
        for category, category_keywords in self.category_mapping.items():
            score = 0
            for keyword in keywords:
                if keyword in category_keywords:
                    score += 1
            category_scores[category] = score
        
        # Return the category with highest score, default to 'measurement'
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return 'measurement'
    
    def generate_title_from_folder(self, folder_name):
        """Generate a human-readable title from folder name"""
        # Clean up the folder name
        title = folder_name.replace('_', ' ').replace('-', ' ')
        
        # Capitalize words properly
        words = title.split()
        capitalized_words = []
        
        for word in words:
            if word.lower() in ['a', 'an', 'the', 'of', 'in', 'to', 'for', 'with', 'by']:
                capitalized_words.append(word.lower())
            else:
                capitalized_words.append(word.capitalize())
        
        return ' '.join(capitalized_words)
    
    def generate_description_from_title(self, title, category):
        """Generate a description based on title and category"""
        descriptions = {
            'time': f'Calculate and convert time-related measurements from your {title} query',
            'volume': f'Convert between different volume units based on your {title} question', 
            'weight': f'Convert between different weight and mass units for your {title} needs',
            'length': f'Convert between different length and distance units from your {title}',
            'measurement': f'Get accurate measurements and calculations for your {title} question',
            'calculator': f'Quick and accurate calculations for your {title} query',
            'countdown': f'Real-time countdown and time calculation for your {title}',
            'conversions': f'Unit conversion tool for your {title} measurements'
        }
        
        return descriptions.get(category, f'Find accurate answers to your {title} question')

    def check_sharing_enabled(self, folder_path):
        """Check if sharing functionality is enabled in the tool"""
        try:
            index_file = folder_path / 'index.html'
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for sharing indicators
                    sharing_indicators = [
                        'share-utils.js',
                        'HowManyQShare',
                        'shareCountdown',
                        'shareOnTwitter',
                        'shareOnFacebook',
                        'copyResults',
                        'class="share-section"',
                        'id="shareButtons"'
                    ]
                    return any(indicator in content for indicator in sharing_indicators)
        except Exception as e:
            print(f"Warning: Could not check sharing status for {folder_path}: {e}")
        return False

    def generate_share_text(self, folder_name, title, category):
        """Generate appropriate share text for the tool"""
        share_texts = {
            'time': f'Check out this {title} calculator! 🕐',
            'volume': f'Convert volumes easily with this {title} tool! 🧪',
            'weight': f'Calculate weights with this {title} calculator! ⚖️',
            'length': f'Measure distances with this {title} tool! 📏',
            'measurement': f'Get accurate measurements with this {title} calculator! 📊'
        }

        return share_texts.get(category, f'Try this amazing {title} calculator! 🧮')
    
    def generate_tool_data(self, folder_path):
        """Generate tool data for a single folder"""
        folder_name = folder_path.name
        keywords = self.extract_keywords_from_folder(folder_name)
        category = self.determine_category(folder_name, keywords)
        title = self.generate_title_from_folder(folder_name)
        description = self.generate_description_from_title(title, category)
        
        # Generate a unique ID
        tool_id = re.sub(r'[^a-zA-Z0-9]', '', folder_name.lower())
        
        return {
            'id': tool_id,
            'title': title,
            'description': description,
            'category': category,
            'url': f'{folder_name}/index.html',
            'folder_name': folder_name,
            'keywords': keywords,
            'icon': self.icon_mapping.get(category, '🧮'),
            'sharing_enabled': self.check_sharing_enabled(folder_path),
            'share_text': self.generate_share_text(folder_name, title, category)
        }
    
    def discover_tools(self):
        """Discover all tools by scanning for index.html files"""
        tools = []
        
        # Check current directory
        current_index = self.base_path / 'index.html'
        if current_index.exists() and current_index.is_file():
            # This is the main navigation page, skip it
            pass
        
        # Scan all subdirectories
        for item in self.base_path.iterdir():
            if item.is_dir() and item.name not in self.excluded_folders:
                index_file = item / 'index.html'
                if index_file.exists() and index_file.is_file():
                    tool_data = self.generate_tool_data(item)
                    tools.append(tool_data)
        
        return tools
    
    def generate_navigation_data(self):
        """Generate complete navigation data"""
        tools = self.discover_tools()
        
        # Generate categories based on discovered tools
        categories = {}
        for tool in tools:
            category = tool['category']
            if category not in categories:
                categories[category] = {
                    'name': category.title(),
                    'description': f'Tools for {category} calculations and conversions',
                    'icon': self.icon_mapping.get(category, '🧮'),
                    'tools': []
                }
            categories[category]['tools'].append(tool)
        
        # Calculate statistics
        stats = {
            'total_tools': len(tools),
            'total_categories': len(categories),
            'last_updated': '2025-11-06',
            'last_scan': '2025-11-06 20:12:18'
        }
        
        return {
            'tools': tools,
            'categories': categories,
            'statistics': stats,
            'metadata': {
                'version': '1.0',
                'generator': 'HowManyQ Navigation Generator v1.0',
                'scan_time': '2025-11-06 20:12:18'
            }
        }
    
    def save_navigation_data(self, output_file='navigation_data.json'):
        """Save the navigation data to a JSON file"""
        navigation_data = self.generate_navigation_data()
        output_path = self.base_path / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(navigation_data, f, indent=2, ensure_ascii=False)
        
        return output_path, navigation_data

def main():
    """Main function to generate navigation data"""
    generator = NavigationGenerator()
    
    print("🔍 HowManyQ Navigation Generator")
    print("=" * 50)
    
    # Generate navigation data
    output_path, data = generator.save_navigation_data()
    
    print(f"✅ Navigation data generated successfully!")
    print(f"📁 Output file: {output_path}")
    print(f"🔢 Total tools discovered: {data['statistics']['total_tools']}")
    print(f"📂 Total categories: {data['statistics']['total_categories']}")
    print()
    
    print("📋 Discovered Tools:")
    print("-" * 30)
    for i, tool in enumerate(data['tools'], 1):
        sharing_status = "✅" if tool.get('sharing_enabled') else "❌"
        print(f"{i:2d}. {tool['title']} ({tool['category']}) {sharing_status}")
        print(f"    📁 {tool['folder_name']}/index.html")
        if tool.get('sharing_enabled'):
            print(f"    🔄 Sharing enabled")
        print()

    print("📂 Categories Found:")
    print("-" * 20)
    for category, info in data['categories'].items():
        print(f"{category.title()}: {len(info['tools'])} tools")

    # Sharing statistics
    sharing_enabled_count = sum(1 for tool in data['tools'] if tool.get('sharing_enabled'))
    print(f"\n🔄 Sharing Statistics:")
    print(f"Tools with sharing enabled: {sharing_enabled_count}/{data['statistics']['total_tools']}")
    print(f"Sharing coverage: {(sharing_enabled_count/data['statistics']['total_tools']*100):.1f}%")
    
    return data

if __name__ == "__main__":
    main()
