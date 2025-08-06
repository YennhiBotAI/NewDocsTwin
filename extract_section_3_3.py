#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import re

def extract_section_3_3_content():
    """Extract comprehensive content from Section 3.3 HTML file"""
    
    html_file = "3.3. Quản lý công việc với _Projects_ _ Twin AI Docs.html"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        print("Section 3.3 content extracted:")
        print("=" * 80)
        
        # Extract main content by looking for paragraphs with the right classes
        main_paragraphs = soup.find_all('p', class_=re.compile(r'mx-auto.*text-start'))
        
        for i, p in enumerate(main_paragraphs):
            text = p.get_text().strip()
            if text and len(text) > 10:
                print(f"\nParagraph {i+1}:")
                print(f"- {text}")
        
        # Look for any section headers
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'], class_=re.compile(r'text-.*heading|font-semibold|font-bold'))
        
        print(f"\n{'-'*40}")
        print("HEADERS FOUND:")
        for header in headers:
            header_text = header.get_text().strip()
            if header_text and 'Quản lý công việc với' in header_text:
                print(f"- MAIN TITLE: {header_text}")
            elif header_text and len(header_text) > 3:
                print(f"- {header.name.upper()}: {header_text}")
        
        # Look for lists
        lists = soup.find_all(['ul', 'ol'])
        print(f"\n{'-'*40}")
        print("LISTS FOUND:")
        for i, ul in enumerate(lists):
            list_items = ul.find_all('li')
            if list_items:
                print(f"\nList {i+1}:")
                for li in list_items:
                    li_text = li.get_text().strip()
                    if li_text:
                        print(f"  • {li_text}")
                        
        # Look for emphasized text (bold, strong)
        emphasis = soup.find_all(['strong', 'b'])
        print(f"\n{'-'*40}")
        print("EMPHASIZED TEXT:")
        for emp in emphasis:
            emp_text = emp.get_text().strip()
            if emp_text and len(emp_text) > 2:
                print(f"**{emp_text}**")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"Error extracting content: {e}")
        return None

if __name__ == "__main__":
    print("Extracting Section 3.3 content...")
    extract_section_3_3_content()
