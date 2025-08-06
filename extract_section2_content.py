#!/usr/bin/env python3
import re
from bs4 import BeautifulSoup

def extract_section2_content():
    """Extract Section 2 content from HTML file"""
    
    try:
        with open('2. GÓI DỊCH VỤ VÀ THANH TOÁN _ Twin AI Docs.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the main content
        main_content = soup.find('div', class_="grid [&>*+*]:mt-5 whitespace-pre-wrap")
        
        if not main_content:
            print("Could not find main content div")
            return
            
        # Extract text content
        text_content = []
        
        # Get the intro paragraph
        intro_p = main_content.find('p')
        if intro_p:
            intro_text = intro_p.get_text(strip=True)
            text_content.append(intro_text)
            
        # Get the section cards
        card_container = main_content.find('div', class_=re.compile(r'inline-grid.*grid-cols'))
        if card_container:
            cards = card_container.find_all('div', class_=re.compile(r'group.*grid'))
            
            for card in cards:
                # Get card title
                title_elem = card.find('div', class_=re.compile(r'font-semibold'))
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    text_content.append(f"## {title}")
                    
                # Get card description
                desc_elem = card.find('div', class_=re.compile(r'text-sm.*text-muted'))
                if desc_elem:
                    desc = desc_elem.get_text(strip=True)
                    text_content.append(desc)
                    text_content.append("")  # Add blank line
        
        # Generate markdown content
        markdown_content = f"""# 2. Gói Dịch vụ và Thanh toán

{text_content[0]}

{chr(10).join(text_content[1:])}

## Trong phần này

### [2.1. Tổng quan các Gói dịch vụ](/pricing/service-packages)
Tìm hiểu về các gói dịch vụ và tính năng tương ứng để lựa chọn gói phù hợp nhất với nhu cầu của bạn.

### [2.2. Hướng dẫn Thanh toán](/pricing/payment-guide)
Hướng dẫn chi tiết về các phương thức thanh toán, gia hạn và quản lý thanh toán.
"""
        
        print("Section 2 content extracted:")
        print("=" * 60)
        print(markdown_content)
        print("=" * 60)
        
        return markdown_content
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    extract_section2_content()
