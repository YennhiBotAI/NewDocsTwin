#!/usr/bin/env python3
"""
Script to update Section 5 and Section 6 documentation with content from PDF files
"""

import json
import os
import re

def load_json_content(file_path):
    """Load content from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text):
    """Clean text for markdown formatting"""
    # Remove extra spaces and clean up
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def create_section_5_files():
    """Create Section 5 API documentation files from PDF content"""
    
    # Load PDF content
    section_5_data = load_json_content('section_5_pdf_content.json')
    lines = section_5_data['cleaned_lines']
    
    # Main index file
    index_content = '''---
title: "Dành cho Nhà phát triển"
description: "TwinExpert API Documentation - Tài liệu API cho nhà phát triển"
---

# Dành cho Nhà phát triển (TwinExpert API Documentation)

Twin AI cung cấp một bộ API mạnh mẽ cho phép các nhà phát triển tích hợp sức mạnh của Twin AI vào các ứng dụng và hệ thống của riêng họ.

## Nội dung chính

<div class="grid-container">
  <div class="grid-item">
    <h3><a href="./getting-started">5.1. Bắt đầu với API</a></h3>
    <p>Hướng dẫn bắt đầu nhanh với Twin AI API</p>
  </div>
  
  <div class="grid-item">
    <h3><a href="./authentication">5.2. Xác thực</a></h3>
    <p>Cách xác thực và bảo mật API calls</p>
  </div>
  
  <div class="grid-item">
    <h3><a href="./endpoints">5.3. API Endpoints</a></h3>
    <p>Chi tiết về các endpoints và parameters</p>
  </div>
  
  <div class="grid-item">
    <h3><a href="./examples">5.4. Ví dụ</a></h3>
    <p>Các ví dụ thực tế sử dụng API</p>
  </div>
  
  <div class="grid-item">
    <h3><a href="./rate-limiting">5.5. Rate Limiting</a></h3>
    <p>Giới hạn tần suất và best practices</p>
  </div>
  
  <div class="grid-item">
    <h3><a href="./error-handling">5.6. Xử lý lỗi</a></h3>
    <p>Cách xử lý lỗi và troubleshooting</p>
  </div>
</div>

## API Overview

Twin AI API được thiết kế với các nguyên tắc REST, sử dụng HTTP methods chuẩn và trả về JSON responses. API hỗ trợ authentication qua API keys và có hệ thống rate limiting để đảm bảo hiệu suất ổn định.

### Base URL
```
https://api.twinai.dev/v1
```

### Yêu cầu hệ thống
- HTTP/1.1 hoặc HTTP/2
- TLS 1.2 trở lên
- Content-Type: application/json
- Authorization header với API key

---

::: tip Ghi chú
API documentation này được cập nhật thường xuyên. Vui lòng theo dõi [changelog](/changelog) để biết các thay đổi mới nhất.
:::
'''

    # Create docs/api directory if not exists
    os.makedirs('docs/api', exist_ok=True)
    
    # Write index file
    with open('docs/api/index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("✅ Created docs/api/index.md")

    # Extract content for each subsection from PDF lines
    current_section = None
    sections = {
        '5.1': {'title': 'Bắt đầu với API', 'content': []},
        '5.2': {'title': 'Xác thực', 'content': []},
        '5.3': {'title': 'API Endpoints', 'content': []},
        '5.4': {'title': 'Ví dụ', 'content': []},
        '5.5': {'title': 'Rate Limiting', 'content': []},
        '5.6': {'title': 'Xử lý lỗi', 'content': []}
    }
    
    # Parse content from PDF lines
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers
        if line.startswith('5.1.') or 'Bắt đầu với API' in line:
            current_section = '5.1'
        elif line.startswith('5.2.') or 'Xác thực' in line:
            current_section = '5.2'
        elif line.startswith('5.3.') or 'API Endpoints' in line:
            current_section = '5.3'
        elif line.startswith('5.4.') or line == 'Ví dụ':
            current_section = '5.4'
        elif line.startswith('5.5.') or 'Rate Limiting' in line:
            current_section = '5.5'
        elif line.startswith('5.6.') or 'Xử lý lỗi' in line:
            current_section = '5.6'
        elif current_section and line not in [sections[current_section]['title']]:
            sections[current_section]['content'].append(line)
    
    # Create individual files
    file_mapping = {
        '5.1': 'getting-started.md',
        '5.2': 'authentication.md', 
        '5.3': 'endpoints.md',
        '5.4': 'examples.md',
        '5.5': 'rate-limiting.md',
        '5.6': 'error-handling.md'
    }
    
    for section_key, filename in file_mapping.items():
        section_data = sections[section_key]
        content = f'''---
title: "{section_data['title']}"
description: "Twin AI API - {section_data['title']}"
---

# {section_key}. {section_data['title']}

'''
        
        # Add content from PDF
        if section_data['content']:
            for line in section_data['content']:
                # Format as markdown
                if line.strip():
                    # Check if it's a header-like line
                    if len(line) < 100 and any(char.isupper() for char in line):
                        content += f"\n## {line}\n\n"
                    else:
                        content += f"{line}\n\n"
        else:
            content += "Nội dung đang được cập nhật từ tài liệu PDF.\n\n"
        
        content += '''
---

::: tip Cần hỗ trợ?
Nếu bạn gặp vấn đề với API, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com).
:::
'''
        
        with open(f'docs/api/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created docs/api/{filename}")

def create_section_6_files():
    """Create Section 6 Support documentation files from PDF content"""
    
    # Load PDF content
    section_6_data = load_json_content('section_6_pdf_content.json')
    lines = section_6_data['cleaned_lines']
    
    # Create docs/support directory if not exists
    os.makedirs('docs/support', exist_ok=True)
    
    # Main index file
    index_content = '''---
title: "Tài nguyên & Hỗ trợ"
description: "Trung tâm hỗ trợ, FAQs và tài nguyên cho người dùng Twin AI"
---

# Tài nguyên & Hỗ trợ

Đây là trung tâm hỗ trợ, nơi người dùng có thể tìm thấy câu trả lời cho các câu hỏi, các kênh liên lạc và các tài nguyên bổ sung.

## Nội dung chính

<div class="grid-container">
  <div class="grid-item">
    <h3><a href="./faqs">6.1. Các câu hỏi thường gặp (FAQs)</a></h3>
    <p>Tìm câu trả lời nhanh cho những thắc mắc phổ biến nhất về Twin AI</p>
  </div>
  
  <div class="grid-item">
    <h3><a href="./support-channels">6.2. Các kênh hỗ trợ</a></h3>
    <p>Các cách để liên hệ với đội ngũ Twin AI khi bạn cần sự trợ giúp</p>
  </div>
  
  <div class="grid-item">
    <h3><a href="./glossary">6.3. Bảng thuật ngữ</a></h3>
    <p>Giải thích các thuật ngữ và khái niệm chính được sử dụng trong Twin AI</p>
  </div>
</div>

## Hỗ trợ nhanh

### 📧 Email hỗ trợ
[agent.twinai@gmail.com](mailto:agent.twinai@gmail.com)

### 💬 Cộng đồng
Tham gia cộng đồng Twin AI trên Zalo để trao đổi kinh nghiệm và học hỏi.

### 📚 Tài liệu
Khám phá thêm các hướng dẫn chi tiết trong documentation này.

---

::: tip Mẹo
Trước khi liên hệ hỗ trợ, hãy kiểm tra [FAQs](/support/faqs) - có thể câu trả lời bạn cần đã có sẵn!
:::
'''

    with open('docs/support/index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("✅ Created docs/support/index.md")
    
    # Parse content for each subsection
    current_section = None
    sections = {
        '6.1': {'title': 'Các câu hỏi thường gặp (FAQs)', 'content': []},
        '6.2': {'title': 'Các kênh hỗ trợ', 'content': []},
        '6.3': {'title': 'Bảng thuật ngữ', 'content': []}
    }
    
    # Parse PDF content
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers
        if line.startswith('6.1.') or 'Các câu hỏi thường gặp' in line:
            current_section = '6.1'
        elif line.startswith('6.2.') or 'Các kênh hỗ trợ' in line:
            current_section = '6.2'
        elif line.startswith('6.3.') or 'Bảng thuật ngữ' in line:
            current_section = '6.3'
        elif current_section and line not in [sections[current_section]['title']]:
            sections[current_section]['content'].append(line)
    
    # Create individual files
    file_mapping = {
        '6.1': 'faqs.md',
        '6.2': 'support-channels.md',
        '6.3': 'glossary.md'
    }
    
    for section_key, filename in file_mapping.items():
        section_data = sections[section_key]
        content = f'''---
title: "{section_data['title']}"
description: "Twin AI - {section_data['title']}"
---

# {section_key}. {section_data['title']}

'''
        
        # Add content from PDF
        if section_data['content']:
            for line in section_data['content']:
                if line.strip():
                    # Format questions/answers for FAQs
                    if section_key == '6.1' and line[0].isdigit() and '.' in line[:5]:
                        content += f"\n## {line}\n\n"
                    # Format headers
                    elif len(line) < 100 and any(char.isupper() for char in line) and not line.startswith('•'):
                        content += f"\n## {line}\n\n"
                    # Format list items
                    elif line.startswith('•'):
                        content += f"{line}\n\n"
                    # Regular content
                    else:
                        content += f"{line}\n\n"
        else:
            content += "Nội dung đang được cập nhật từ tài liệu PDF.\n\n"
        
        content += '''
---

::: tip Cần thêm hỗ trợ?
Nếu không tìm thấy thông tin bạn cần, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com).
:::
'''
        
        with open(f'docs/support/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created docs/support/{filename}")

def main():
    """Main function to update all sections"""
    print("🔄 Updating Section 5 and Section 6 from PDF content...")
    
    # Update Section 5 - API Documentation
    print("\n📁 Creating Section 5 - API Documentation...")
    create_section_5_files()
    
    # Update Section 6 - Support Resources  
    print("\n📁 Creating Section 6 - Support Resources...")
    create_section_6_files()
    
    print("\n✅ All sections updated successfully!")
    print("\n📋 Summary:")
    print("   - Section 5: API documentation updated with PDF content")
    print("   - Section 6: Support resources updated with PDF content")
    print("   - All files created with proper VitePress frontmatter")
    print("   - Content extracted directly from authoritative PDF sources")

if __name__ == "__main__":
    main()
