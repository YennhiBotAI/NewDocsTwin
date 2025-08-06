#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 4 Teams Content Extraction Script
Extracts and processes content from Section 4 Teams HTML file
Following the established systematic methodology for 100% accuracy
"""

import os
from bs4 import BeautifulSoup
import json

def extract_section_4_content():
    """Extract and analyze Section 4 Teams content from HTML file"""
    
    html_file = "/workspaces/NewDocsTwin/4. QUẢN LÝ TEAMS CỦA BẠN _ Twin AI Docs.html"
    
    print("🔍 SECTION 4 TEAMS CONTENT EXTRACTION")
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
    main_content = soup.find('main') or soup.find('div', class_='main-content') or soup.find('article')
    
    if not main_content:
        # Try to find content by common patterns
        content_selectors = [
            'div[class*="content"]',
            'div[class*="article"]',
            'div[class*="docs"]',
            'section[class*="content"]'
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
    
    if not main_content:
        print("⚠️ Could not find main content area, using body")
        main_content = soup.find('body')
    
    print(f"📍 Content area found: {main_content.name} with class: {main_content.get('class', [])}")
    
    # Extract all headings
    print("\n📋 HEADINGS STRUCTURE:")
    print("-" * 40)
    headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    for i, heading in enumerate(headings):
        level = heading.name
        text = heading.get_text().strip()
        print(f"{level.upper()}: {text}")
    
    # Extract all paragraphs and content blocks
    print("\n📝 CONTENT BLOCKS:")
    print("-" * 40)
    
    content_blocks = []
    
    # Find all text-containing elements
    text_elements = main_content.find_all(['p', 'div', 'span', 'li', 'td', 'th'])
    
    for element in text_elements:
        text = element.get_text().strip()
        if text and len(text) > 10:  # Filter out very short text
            # Clean up the text
            text = ' '.join(text.split())
            
            # Categorize by parent context
            parent_classes = []
            current = element
            while current and current.name != 'body':
                if current.get('class'):
                    parent_classes.extend(current.get('class'))
                current = current.parent
            
            content_blocks.append({
                'text': text,
                'element': element.name,
                'classes': parent_classes,
                'length': len(text)
            })
    
    # Sort by length and relevance
    content_blocks.sort(key=lambda x: x['length'], reverse=True)
    
    print(f"Found {len(content_blocks)} content blocks")
    print("\n🎯 TOP CONTENT BLOCKS (by relevance):")
    print("-" * 50)
    
    for i, block in enumerate(content_blocks[:20]):  # Show top 20
        print(f"\n[{i+1}] Element: {block['element']} | Length: {block['length']}")
        print(f"Classes: {', '.join(block['classes'][:3]) if block['classes'] else 'None'}")
        print(f"Text: {block['text'][:200]}{'...' if len(block['text']) > 200 else ''}")
    
    # Look for specific Teams-related content
    print("\n🏢 TEAMS-SPECIFIC CONTENT:")
    print("-" * 40)
    
    teams_keywords = [
        'team', 'đội ngũ', 'thành viên', 'member', 'collaboration',
        'cộng tác', 'permission', 'quyền hạn', 'role', 'vai trò',
        'manage', 'quản lý', 'invite', 'mời', 'join', 'tham gia'
    ]
    
    teams_content = []
    for block in content_blocks:
        text_lower = block['text'].lower()
        if any(keyword in text_lower for keyword in teams_keywords):
            teams_content.append(block)
    
    print(f"Found {len(teams_content)} Teams-related content blocks:")
    
    for i, block in enumerate(teams_content[:10]):  # Show top 10 Teams content
        print(f"\n[T{i+1}] {block['text'][:300]}{'...' if len(block['text']) > 300 else ''}")
    
    # Extract navigation/menu items
    print("\n📐 NAVIGATION & MENU ITEMS:")
    print("-" * 40)
    
    nav_elements = main_content.find_all(['nav', 'ul', 'ol'])
    for nav in nav_elements:
        links = nav.find_all('a')
        if links:
            print(f"\nNavigation block with {len(links)} links:")
            for link in links[:5]:  # Show first 5 links
                text = link.get_text().strip()
                href = link.get('href', '')
                if text:
                    print(f"  • {text} → {href}")
    
    # Save extracted content to file
    output_data = {
        'title': title.get_text().strip() if title else '',
        'headings': [{'level': h.name, 'text': h.get_text().strip()} for h in headings],
        'content_blocks': content_blocks[:50],  # Save top 50 blocks
        'teams_content': teams_content[:20]  # Save top 20 Teams blocks
    }
    
    output_file = "/workspaces/NewDocsTwin/section_4_extracted_content.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Content saved to: {output_file}")
    
    return output_data

if __name__ == "__main__":
    try:
        result = extract_section_4_content()
        print("\n✅ Section 4 Teams content extraction completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during extraction: {str(e)}")
        import traceback
        traceback.print_exc()
