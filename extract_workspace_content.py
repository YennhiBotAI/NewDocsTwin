#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re

def extract_workspace_content():
    # Read the HTML file
    with open("3.1. Không gian làm việc của bạn_ _ Twin AI Docs.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find main content area
    main_content = soup.find('main')
    if not main_content:
        print("No main content found")
        return
    
    # Extract all paragraphs, headings, and other content
    content_elements = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'ol', 'ul', 'li', 'div'])
    
    extracted_content = []
    
    for elem in content_elements:
        text = elem.get_text(strip=True)
        if text and len(text) > 10:  # Filter out very short text
            # Clean up extra whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Skip navigation and metadata
            skip_patterns = [
                'Previous', 'Next', 'Last updated',
                'Ask', 'Export as PDF', 'Powered by GitBook',
                'breadcrumb', 'navigation', '3. NỀN TẢNG (THE BASICS)',
                'Twin AI Docs'
            ]
            
            if not any(pattern in text for pattern in skip_patterns):
                extracted_content.append(text)
    
    # Print the extracted content
    print("=== EXTRACTED WORKSPACE CONTENT ===")
    for i, content in enumerate(extracted_content, 1):
        print(f"{i}. {content}")
        print()

if __name__ == "__main__":
    extract_workspace_content()
