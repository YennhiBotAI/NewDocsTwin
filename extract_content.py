#!/usr/bin/env python3
"""
Script to extract content from GitBook HTML files and convert to markdown
"""

import os
import re
import html
from pathlib import Path
from bs4 import BeautifulSoup

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_content_from_html(file_path):
    """Extract main content from GitBook HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to find content in the complex GitBook structure
    # Look for patterns that contain Vietnamese text
    patterns = [
        r'"children":"([^"]+)"',
        r'"children":\["([^"]+)"\]',
        r'text-start justify-self-start">([^<]+)<',
        r'class="[^"]*text-[^"]*">([^<]+)<'
    ]
    
    extracted_text = []
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            
            # Skip if it's not Vietnamese content or is too short
            if len(match) < 10:
                continue
            
            # Check if it contains Vietnamese characters or common Vietnamese words
            vietnamese_indicators = ['đ', 'ă', 'â', 'ê', 'ô', 'ơ', 'ư', 'ầ', 'ấ', 'ậ', 'ẩ', 'ả', 
                                   'với', 'của', 'trong', 'những', 'như', 'được', 'tôi', 'chúng', 'mình']
            
            if any(indicator in match.lower() for indicator in vietnamese_indicators):
                cleaned = clean_text(match)
                if cleaned and len(cleaned) > 20:
                    extracted_text.append(cleaned)
    
    # Get title from meta tags or h1
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = ""
    if title_match:
        title = clean_text(title_match.group(1)).replace(" | Twin AI Docs", "")
    
    return title, extracted_text

def main():
    """Main function to process all HTML files"""
    workspace_path = Path("/workspaces/NewDocsTwin")
    html_files = list(workspace_path.glob("*.html"))
    
    # Filter main content files (exclude _files directories)
    main_files = [f for f in html_files if "_files" not in str(f)]
    
    print(f"Found {len(main_files)} HTML files to process:")
    
    for html_file in main_files:
        print(f"\n=== Processing: {html_file.name} ===")
        
        try:
            title, content_lines = extract_content_from_html(html_file)
            
            print(f"Title: {title}")
            print(f"Found {len(content_lines)} content pieces")
            
            # Show first few content pieces
            for i, line in enumerate(content_lines[:5]):
                print(f"  {i+1}: {line[:100]}...")
                
        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")

if __name__ == "__main__":
    main()
