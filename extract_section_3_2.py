#!/usr/bin/env python3
"""
Script để extract nội dung từ Section 3.2 - Nghệ thuật Đối thoại cùng Twin AI
"""

import re
from bs4 import BeautifulSoup

def extract_conversation_art_content(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Tìm title chính
    title_element = soup.find('h1')
    title = title_element.get_text(strip=True) if title_element else "3.2. Nghệ thuật Đối thoại cùng Twin AI"
    
    # Extract nội dung chính
    content_sections = []
    
    # Tìm tất cả paragraph và heading elements
    main_content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'li', 'div'], 
                                string=re.compile(r'(Giao tiếp|nguyên tắc|VAI TRÒ|MỤC TIÊU|BỐI CẢNH|YÊU CẦU|File Attachment|Tệp đính kèm)', re.IGNORECASE))
    
    # Extract text content từ các element tìm được
    extracted_content = []
    for element in main_content:
        text = element.get_text(strip=True)
        if len(text) > 10 and not any(skip in text.lower() for skip in ['javascript', 'css', 'font-family', 'color-scheme']):
            extracted_content.append(text)
    
    # Tìm cụ thể nội dung về nguyên tắc vàng
    golden_rule_pattern = r'nguyên tắc vàng.*?context.*?king|context.*?nguyên tắc vàng'
    
    # Tìm các framework prompt
    framework_patterns = [
        r'\[VAI TRÒ\].*?"',
        r'\[MỤC TIÊU\].*?"', 
        r'\[BỐI CẢNH.*?\].*?"',
        r'\[YÊU CẦU.*?\].*?"'
    ]
    
    # Tìm nội dung về file attachment
    attachment_pattern = r'(File Attachment|Tệp đính kèm|đính kèm file)'
    
    # Parse toàn bộ nội dung để tìm structure
    all_text = soup.get_text()
    
    # Tách các phần chính
    sections = {
        'title': title,
        'introduction': '',
        'golden_rule': '',
        'framework': [],
        'file_attachment': '',
        'best_practices': []
    }
    
    # Tìm phần introduction
    intro_match = re.search(r'Giao tiếp hiệu quả.*?Twin AI\..*?sắc bén\.', all_text, re.DOTALL)
    if intro_match:
        sections['introduction'] = intro_match.group()
    
    # Tìm nguyên tắc vàng
    golden_match = re.search(r'nguyên tắc vàng.*?context.*?king.*?cụ thể', all_text, re.DOTALL | re.IGNORECASE)
    if golden_match:
        sections['golden_rule'] = golden_match.group()
    
    # Tìm framework elements
    for pattern in framework_patterns:
        matches = re.findall(pattern, all_text, re.IGNORECASE)
        sections['framework'].extend(matches)
    
    # Tìm file attachment section
    attachment_match = re.search(r'(Sử dụng tệp đính kèm|File Attachment).*?(?=\n\n|\Z)', all_text, re.DOTALL | re.IGNORECASE)
    if attachment_match:
        sections['file_attachment'] = attachment_match.group()
    
    return sections

def format_to_markdown(sections):
    """Chuyển đổi sections thành markdown format"""
    
    md_content = f"# {sections['title']}\n\n"
    
    if sections['introduction']:
        md_content += f"{sections['introduction']}\n\n"
    
    if sections['golden_rule']:
        md_content += "## Nguyên tắc vàng: Context is King\n\n"
        md_content += f"{sections['golden_rule']}\n\n"
    
    if sections['framework']:
        md_content += "## Framework prompting hiệu quả\n\n"
        md_content += "Cấu trúc một prompt hiệu quả:\n\n"
        for item in sections['framework']:
            md_content += f"- {item}\n"
        md_content += "\n"
    
    if sections['file_attachment']:
        md_content += "## Sử dụng tệp đính kèm (File Attachment)\n\n"
        md_content += f"{sections['file_attachment']}\n\n"
    
    return md_content

if __name__ == "__main__":
    html_file = "3.2. Nghệ thuật Đối thoại cùng Twin AI_ _ Twin AI Docs.html"
    
    try:
        sections = extract_conversation_art_content(html_file)
        
        print("=== EXTRACTED CONTENT ===")
        print(f"Title: {sections['title']}")
        print(f"Introduction: {sections['introduction'][:100]}..." if sections['introduction'] else "No introduction found")
        print(f"Golden Rule: {sections['golden_rule'][:100]}..." if sections['golden_rule'] else "No golden rule found")
        print(f"Framework items: {len(sections['framework'])}")
        print(f"File attachment: {sections['file_attachment'][:100]}..." if sections['file_attachment'] else "No file attachment section found")
        
        # Generate markdown
        markdown_content = format_to_markdown(sections)
        
        with open("section_3_2_extracted.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print("\n=== SUCCESS ===")
        print("Content extracted and saved to section_3_2_extracted.md")
        
    except FileNotFoundError:
        print(f"Error: File {html_file} not found")
    except Exception as e:
        print(f"Error extracting content: {e}")
