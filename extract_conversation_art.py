#!/usr/bin/env python3
import re
from bs4 import BeautifulSoup

def extract_conversation_art_content():
    """Extract Section 3.2 content from HTML file"""
    
    try:
        with open('3.2. Nghệ thuật Đối thoại cùng Twin AI_ _ Twin AI Docs.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the main content
        main_content = soup.find('main')
        if not main_content:
            print("Could not find main content")
            return
            
        # Extract text content systematically
        content_blocks = []
        
        # Get all paragraphs and headings
        elements = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li'])
        
        current_section = ""
        
        for elem in elements:
            text = elem.get_text(strip=True)
            
            # Skip navigation, metadata, and short texts
            if (not text or len(text) < 10 or 
                'Previous' in text or 'Next' in text or 
                'Last updated' in text or 'GitBook' in text or
                'breadcrumb' in text.lower() or
                text == '3.2. Nghệ thuật Đối thoại cùng Twin AI:'):
                continue
                
            # Clean up text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Identify sections by tag
            if elem.name in ['h1', 'h2', 'h3']:
                if text not in content_blocks:  # Avoid duplicates
                    content_blocks.append(f"\n## {text}\n")
                    current_section = text
            elif elem.name == 'p':
                if text not in content_blocks:
                    content_blocks.append(text + "\n")
            elif elem.name in ['ul', 'ol']:
                # Handle lists
                list_items = elem.find_all('li')
                for li in list_items:
                    li_text = li.get_text(strip=True)
                    if li_text and len(li_text) > 5:
                        content_blocks.append(f"- {li_text}")
                content_blocks.append("")  # Add spacing after list
        
        # Generate markdown content
        markdown_content = f"""# 3.2. Nghệ thuật Đối thoại cùng Twin AI

{''.join(content_blocks)}

---

*Để hiểu rõ hơn về cách sử dụng Twin AI hiệu quả, hãy thực hành với các ví dụ và mẹo được chia sẻ ở trên.*
"""
        
        print("Section 3.2 content extracted:")
        print("=" * 80)
        print(markdown_content)
        print("=" * 80)
        
        return markdown_content
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    extract_conversation_art_content()
