#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import csv

def clean_folder_name(name):
    """清理文件夹名称，使其符合文件系统规范"""
    # 移除前后的空格
    name = name.strip()
    # 替换空格为下划线
    name = name.replace(' ', '_')
    # 移除或替换特殊字符
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # 移除连字符两边的空格并替换为下划线
    name = re.sub(r'\s*-\s*', '_', name)
    # 移除多余的连字符
    name = re.sub(r'_+', '_', name)
    # 移除首尾的下划线
    name = name.strip('_')
    # 确保名称不为空
    if not name:
        name = "unnamed_folder"
    return name

def create_folders_from_keywords():
    """从questions.md文件中读取关键词并创建文件夹"""
    
    # 读取questions.md文件
    with open('questions.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 解析表格
    lines = content.split('\n')
    keywords = []
    
    # 跳过表头，读取关键词
    for line in lines[2:]:  # 跳过前两行（表头和分隔行）
        if '|' in line:
            parts = [part.strip() for part in line.split('|')]
            if len(parts) >= 3 and parts[1].isdigit():  # 确保是数据行
                keyword = parts[2].strip()
                if keyword:  # 确保关键词不为空
                    keywords.append(keyword)
    
    print(f"找到 {len(keywords)} 个关键词")
    
    # 创建文件夹
    created_folders = []
    failed_folders = []
    
    for i, keyword in enumerate(keywords, 1):
        folder_name = clean_folder_name(keyword)
        try:
            os.makedirs(folder_name, exist_ok=True)
            created_folders.append((i, keyword, folder_name))
            print(f"创建文件夹 {i:3d}: {folder_name}")
        except Exception as e:
            failed_folders.append((i, keyword, folder_name, str(e)))
            print(f"创建文件夹失败 {i:3d}: {folder_name} - 错误: {e}")
    
    print(f"\n总结:")
    print(f"成功创建: {len(created_folders)} 个文件夹")
    print(f"创建失败: {len(failed_folders)} 个文件夹")
    
    if failed_folders:
        print(f"\n失败的文件夹:")
        for item in failed_folders:
            print(f"  {item[1]} -> {item[2]}: {item[3]}")
    
    return created_folders, failed_folders

if __name__ == "__main__":
    create_folders_from_keywords()
