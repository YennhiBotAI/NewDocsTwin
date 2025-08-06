#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 4.1 Team Management Content Extraction
Extracts content from 4.1 Teams HTML file for verification
"""

import os
from bs4 import BeautifulSoup
import json

def extract_section_4_1_content():
    """Extract Section 4.1 Team Management content"""
    
    html_file = "/workspaces/NewDocsTwin/4.1. Quản lý Đội ngũ (Teams)_ _ Twin AI Docs.html"
    
    print("🔍 SECTION 4.1 TEAM MANAGEMENT EXTRACTION")
    print("=" * 60)
    
    # Read HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract page title
    title = soup.find('title')
    if title:
        print(f"📄 PAGE TITLE: {title.get_text().strip()}")
    
    # Find main content area
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    
    if not main_content:
        print("⚠️ Could not find main content area, using body")
        main_content = soup.find('body')
    
    # Extract all headings
    print("\n📋 HEADINGS STRUCTURE:")
    print("-" * 40)
    headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    for heading in headings:
        level = heading.name
        text = heading.get_text().strip()
        print(f"{level.upper()}: {text}")
    
    # Extract all content blocks
    print("\n📝 CONTENT EXTRACTION:")
    print("-" * 40)
    
    content_blocks = []
    text_elements = main_content.find_all(['p', 'div', 'span', 'li', 'td', 'th'])
    
    for element in text_elements:
        text = element.get_text().strip()
        if text and len(text) > 15:  # Filter meaningful content
            text = ' '.join(text.split())
            content_blocks.append({
                'text': text,
                'element': element.name,
                'length': len(text)
            })
    
    # Sort by length for relevance
    content_blocks.sort(key=lambda x: x['length'], reverse=True)
    
    print(f"Found {len(content_blocks)} content blocks")
    
    # Show top relevant content
    print("\n🎯 TOP RELEVANT CONTENT:")
    print("-" * 40)
    
    for i, block in enumerate(content_blocks[:15]):
        if block['length'] > 50:  # Only meaningful content
            print(f"\n[{i+1}] Length: {block['length']}")
            print(f"Text: {block['text'][:300]}{'...' if len(block['text']) > 300 else ''}")
    
    # Look for team management specific content
    print("\n👥 TEAM MANAGEMENT CONTENT:")
    print("-" * 40)
    
    team_keywords = [
        'mời', 'invite', 'thành viên', 'member', 'quyền', 'permission',
        'vai trò', 'role', 'xóa', 'remove', 'quản lý', 'manage'
    ]
    
    team_content = []
    for block in content_blocks:
        text_lower = block['text'].lower()
        if any(keyword in text_lower for keyword in team_keywords):
            team_content.append(block)
    
    print(f"Found {len(team_content)} team management related blocks:")
    
    for i, block in enumerate(team_content[:10]):
        print(f"\n[T{i+1}] {block['text'][:250]}{'...' if len(block['text']) > 250 else ''}")
    
    # Save to file
    output_data = {
        'title': title.get_text().strip() if title else '',
        'headings': [{'level': h.name, 'text': h.get_text().strip()} for h in headings],
        'content_blocks': content_blocks[:30],
        'team_content': team_content[:15]
    }
    
    output_file = "/workspaces/NewDocsTwin/section_4_1_extracted.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Content saved to: {output_file}")
    
    return output_data

if __name__ == "__main__":
    try:
        result = extract_section_4_1_content()
        print("\n✅ Section 4.1 Team Management extraction completed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
