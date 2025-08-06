#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import re

def extract_comprehensive_content():
    """Extract comprehensive content from Section 3.2 HTML file"""
    
    html_file = "3.2. Nghệ thuật Đối thoại cùng Twin AI_ _ Twin AI Docs.html"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract main content areas
        sections = []
        
        # Main introduction
        intro_text = soup.find('p', class_=re.compile(r'mx-auto.*text-start'))
        if intro_text:
            sections.append(f"**Giao tiếp hiệu quả:** {intro_text.get_text().strip()}")
            
        # Find all section headers and content
        headers = soup.find_all('h4', class_=re.compile(r'text-xl.*heading'))
        
        for header in headers:
            header_text = header.get_text().strip()
            sections.append(f"\n## {header_text}")
            
            # Get content after header
            current = header.next_sibling
            while current and current.name not in ['h1', 'h2', 'h3', 'h4']:
                if hasattr(current, 'get_text'):
                    text = current.get_text().strip()
                    if text and len(text) > 5:
                        # Clean up text
                        text = re.sub(r'\s+', ' ', text)
                        
                        # Handle bullet points for the 4 components
                        if '[VAI TRÒ]' in text or '[MỤC TIÊU]' in text or '[BỐI CẢNH' in text or '[YÊU CẦU' in text:
                            sections.append(f"- **{text}**")
                        else:
                            sections.append(f"\n{text}")
                current = current.next_sibling
        
        # Extract any examples or tips
        strong_elements = soup.find_all('strong')
        for strong in strong_elements:
            if strong.get_text().strip() in ['đính kèm', 'kiến thức dự án']:
                parent_text = strong.parent.get_text().strip()
                if parent_text not in '\n'.join(sections):
                    sections.append(f"\n💡 **Mẹo:** {parent_text}")
        
        return '\n'.join(sections)
        
    except Exception as e:
        print(f"Error extracting content: {e}")
        return None

if __name__ == "__main__":
    print("Extracting comprehensive Section 3.2 content...")
    content = extract_comprehensive_content()
    
    if content:
        print("Content extracted successfully:")
        print("=" * 80)
        print(content)
        print("=" * 80)
        
        # Write to markdown file
        with open('section_3_2_complete.md', 'w', encoding='utf-8') as f:
            f.write(f"# 3.2. Nghệ thuật Đối thoại cùng Twin AI\n\n{content}")
        
        print("\nContent saved to section_3_2_complete.md")
    else:
        print("Failed to extract content")
        sys.exit(1)
