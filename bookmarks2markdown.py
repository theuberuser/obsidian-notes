#!/usr/bin/env python3
"""
Convert exported browser bookmarks HTML to organized Docusaurus markdown files.
"""

import os
import re
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime
import sys

class BookmarkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bookmarks = []
        self.current_folder = []
        self.dl_depth = 0
        self.current_link = None
        self.in_h3 = False
        self.h3_text = ''
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'dl':
            self.dl_depth += 1
            
        elif tag == 'h3':
            # This is a folder/heading
            self.in_h3 = True
            self.h3_text = ''
            
        elif tag == 'a':
            # This is a bookmark link
            self.current_link = {
                'url': attrs_dict.get('href', ''),
                'title': '',
                'add_date': attrs_dict.get('add_date', ''),
                'folder_path': list(self.current_folder)
            }
    
    def handle_endtag(self, tag):
        if tag == 'dl':
            self.dl_depth -= 1
            if self.current_folder:
                self.current_folder.pop()
                
        elif tag == 'h3':
            # Folder name complete, add it to current path
            if self.h3_text:
                self.current_folder.append(self.h3_text)
            self.in_h3 = False
            
        elif tag == 'a':
            if self.current_link:
                self.bookmarks.append(self.current_link)
                self.current_link = None
    
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
            
        if self.in_h3:
            # This is a folder name
            self.h3_text = data
        elif self.current_link:
            # This is a bookmark title
            self.current_link['title'] = data


def sanitize_filename(name):
    """Convert a string to a valid filename."""
    # Replace & with 'and'
    name = name.replace('&', 'and')
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces and special chars with hyphens
    name = re.sub(r'[\s\-]+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    # Lowercase for consistency
    name = name.lower()
    # Limit length
    if len(name) > 100:
        name = name[:100]
    return name or 'bookmarks'


def organize_bookmarks_by_folder(bookmarks):
    """Organize bookmarks into a nested dictionary by folder path."""
    organized = {}
    
    for bookmark in bookmarks:
        folder_path = bookmark['folder_path']
        
        # Navigate to the right place in the tree
        current = organized
        for folder in folder_path:
            if folder not in current:
                current[folder] = {'_bookmarks': [], '_subfolders': {}}
            current = current[folder]['_subfolders']
        
        # Add bookmark at the current level
        if folder_path:
            parent_folder = organized
            for folder in folder_path[:-1]:
                parent_folder = parent_folder[folder]['_subfolders']
            parent_folder[folder_path[-1]]['_bookmarks'].append(bookmark)
        else:
            # Root level bookmark
            if '_root' not in organized:
                organized['_root'] = {'_bookmarks': [], '_subfolders': {}}
            organized['_root']['_bookmarks'].append(bookmark)
    
    return organized


def create_markdown_files(organized, base_path, parent_path=''):
    """Recursively create markdown files from organized bookmarks."""
    created_files = []
    
    for folder_name, content in organized.items():
        if folder_name == '_root':
            # Handle root bookmarks
            if content['_bookmarks']:
                file_path = os.path.join(base_path, 'index.md')
                create_bookmark_file(file_path, 'Bookmarks', content['_bookmarks'], parent_path)
                created_files.append(file_path)
            continue
        
        # Create directory for this folder
        safe_folder_name = sanitize_filename(folder_name)
        folder_path = os.path.join(base_path, safe_folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Create markdown file for bookmarks in this folder
        if content['_bookmarks']:
            file_path = os.path.join(folder_path, 'index.md')
            breadcrumb = f"{parent_path}/{folder_name}" if parent_path else folder_name
            create_bookmark_file(file_path, folder_name, content['_bookmarks'], breadcrumb)
            created_files.append(file_path)
        
        # Recursively handle subfolders
        if content['_subfolders']:
            breadcrumb = f"{parent_path}/{folder_name}" if parent_path else folder_name
            subfolder_files = create_markdown_files(
                content['_subfolders'], 
                folder_path,
                breadcrumb
            )
            created_files.extend(subfolder_files)
    
    return created_files


def create_bookmark_file(file_path, title, bookmarks, breadcrumb):
    """Create a markdown file with Docusaurus frontmatter."""
    # Generate slug from title
    slug = sanitize_filename(title)
    
    # Create frontmatter
    frontmatter = f"""---
title: {title}
sidebar_label: {title}
---

# {title}

"""
    
    # Add bookmarks
    content = frontmatter
    
    for bookmark in bookmarks:
        bm_title = bookmark['title'] or bookmark['url']
        bm_url = bookmark['url']
        
        # Escape curly braces and angle brackets that might be interpreted as MDX
        bm_title = bm_title.replace('{', '\\{').replace('}', '\\}')
        bm_title = bm_title.replace('<', '\\<').replace('>', '\\>')
        
        # Add bookmark as a list item with link
        content += f"- [{bm_title}]({bm_url})\n"
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created: {file_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python bookmarks2markdown.py <bookmarks_file.html>")
        sys.exit(1)

    bookmarks_file = sys.argv[1]
    homedir = os.environ['HOME']
    output_dir = os.path.join(homedir, 'obsidian-notes', 'docs')
    print(f"Reading bookmarks from: {bookmarks_file}")
    
    with open(bookmarks_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse bookmarks
    parser = BookmarkParser()
    parser.feed(html_content)
    
    print(f"Found {len(parser.bookmarks)} bookmarks")
    
    # Organize by folder
    organized = organize_bookmarks_by_folder(parser.bookmarks)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Create markdown files
    print(f"\nCreating markdown files in: {output_dir}")
    created_files = create_markdown_files(organized, output_dir)
    
    print(f"\n✓ Successfully created {len(created_files)} markdown files!")
    print(f"Output directory: {output_dir}")


if __name__ == '__main__':
    main()
