#!/usr/bin/env python3
"""
Script to convert GitBook HTML files to VitePress markdown files
"""

import os
import re
import html
from pathlib import Path
import json

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_title_and_description(content):
    """Extract title and description from HTML meta tags"""
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = ""
    if title_match:
        title = clean_text(title_match.group(1)).replace(" | Twin AI Docs", "")
    
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = ""
    if desc_match:
        description = clean_text(desc_match.group(1))
    
    return title, description

def extract_content_from_html(file_path):
    """Extract main content from GitBook HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title, description = extract_title_and_description(content)
    
    # Look for main content in the rendered HTML section
    main_content_pattern = r'<div class="grid \[&.*?\].*?whitespace-pre-wrap">(.*?)</div><!--/\$-->'
    main_match = re.search(main_content_pattern, content, re.DOTALL)
    
    if main_match:
        # Extract paragraphs from the main content
        paragraphs = []
        main_html = main_match.group(1)
        
        # Extract text from paragraph tags
        p_pattern = r'<p[^>]*>([^<]+(?:<[^/][^>]*>[^<]*</[^>]*>[^<]*)*)</p>'
        p_matches = re.findall(p_pattern, main_html)
        
        for match in p_matches:
            # Clean up the text
            clean_match = re.sub(r'<[^>]+>', '', match)  # Remove HTML tags
            clean_match = clean_text(clean_match)
            
            # Check if it's meaningful Vietnamese content
            if len(clean_match) > 20 and any(char in clean_match for char in 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'):
                paragraphs.append(clean_match)
    
    else:
        # Fallback: extract using JavaScript content patterns
        patterns = [
            r'"children":"([^"]{30,})"',
            r'"children":\["([^"]{30,})"\]',
        ]
        
        paragraphs = []
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                clean_match = clean_text(match)
                # Check for Vietnamese content
                if len(clean_match) > 20 and any(char in clean_match for char in 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'):
                    paragraphs.append(clean_match)
    
    return title, description, paragraphs

def create_markdown_file(title, description, paragraphs, output_path):
    """Create a markdown file from extracted content"""
    content = f"# {title}\n\n"
    
    if description:
        content += f"{description}\n\n"
    
    for para in paragraphs[:10]:  # Limit to first 10 paragraphs
        content += f"{para}\n\n"
    
    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_output_path(filename):
    """Determine output path for markdown file"""
    base_docs = Path("/workspaces/NewDocsTwin/docs")
    
    # Map HTML files to appropriate directories
    mapping = {
        "Welcome to Twin AI": "index.md",
        "Chào mừng đến với Twin AI": "welcome/welcome-to-twin-ai.md",
        "Twin AI hoạt động như thế nào?": "welcome/how-twin-ai-works.md",
        "Twin AI dành cho ai?": "welcome/who-is-twin-ai-for.md",
        "Bắt đầu nhanh (Quickstart):": "welcome/quickstart.md",
        "Lộ trình phát triển (Roadmap)": "welcome/roadmap.md",
        
        "1. KHỞI TẠO VÀ QUẢN LÝ TÀI KHOẢN": "account/index.md",
        "1.1. Đăng ký và Đăng nhập:": "account/registration-login.md",
        "1.2. Thiết lập Hồ sơ cá nhân": "account/profile-setup.md",
        
        "2. GÓI DỊCH VỤ VÀ THANH TOÁN": "pricing/index.md",
        "2.1. Tổng quan các Gói dịch vụ:": "pricing/service-packages.md",
        "2.2. Hướng dẫn Thanh toán": "pricing/payment-guide.md",
        
        "3. NỀN TẢNG (THE BASICS)": "basics/index.md",
        "3.1. Không gian làm việc của bạn:": "basics/workspace.md",
        "3.2. Nghệ thuật Đối thoại cùng Twin AI:": "basics/conversation-art.md",
        "3.3. Quản lý công việc với \"Projects\"": "basics/project-management.md",
        
        "4. QUẢN LÝ TEAMS CỦA BẠN": "teams/index.md",
        "4.1. Quản lý Đội ngũ (Teams):": "teams/team-management.md",
        "4.2. Cộng tác trong \"Projects\":": "teams/project-collaboration.md",
        
        "5. DÀNH CHO NHÀ PHÁT TRIỂN (TwinExpert API Documentation)": "api/index.md",
        "5.1. Bắt đầu với API": "api/getting-started.md",
        "5.2. Xác thực": "api/authentication.md",
        "5.3. API Endpoints": "api/endpoints.md",
        "5.4. Ví dụ": "api/examples.md",
        "5.5. Rate Limiting": "api/rate-limiting.md",
        "5.6. Xử lý lỗi": "api/error-handling.md",
        
        "6. TÀI NGUYÊN & HỖ TRỢ": "support/index.md",
        "6.1. Các câu hỏi thường gặp (FAQs)": "support/faqs.md",
        "6.2. Các kênh hỗ trợ": "support/support-channels.md",
        "6.3. Bảng thuật ngữ": "support/glossary.md",
        
        "Phần 1: Dành cho người mới bắt đầu": "support/faqs/beginners.md",
        "Phần 2: Tìm hiểu về các Gói và Tính năng": "support/faqs/packages-features.md",
        "Phần 3: Dành cho người dùng chuyên sâu": "support/faqs/advanced-users.md",
    }
    
    # Get mapped path or create default
    if filename in mapping:
        return base_docs / mapping[filename]
    else:
        # Create safe filename
        safe_name = re.sub(r'[^\w\s-]', '', filename).strip()
        safe_name = re.sub(r'[-\s]+', '-', safe_name).lower()
        return base_docs / f"{safe_name}.md"

def main():
    """Main function to process all HTML files and create markdown files"""
    workspace_path = Path("/workspaces/NewDocsTwin")
    html_files = list(workspace_path.glob("*.html"))
    
    # Filter main content files (exclude _files directories)
    main_files = [f for f in html_files if "_files" not in str(f)]
    
    print(f"Processing {len(main_files)} HTML files...")
    
    processed = 0
    
    for html_file in main_files:
        try:
            title, description, paragraphs = extract_content_from_html(html_file)
            
            if title and paragraphs:
                output_path = get_output_path(title)
                create_markdown_file(title, description, paragraphs, output_path)
                print(f"✓ Created: {output_path}")
                processed += 1
            else:
                print(f"✗ No content found: {html_file.name}")
                
        except Exception as e:
            print(f"✗ Error processing {html_file.name}: {e}")
    
    print(f"\nCompleted: {processed}/{len(main_files)} files processed successfully")

if __name__ == "__main__":
    main()
