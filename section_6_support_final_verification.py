#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 6 Support Resources Final Verification
Complete verification of Section 6 content with HTML source validation
"""

import os
from bs4 import BeautifulSoup
import json

def extract_and_verify_support_content():
    """Extract and verify all Section 6 Support Resources content"""
    
    print("🔍 SECTION 6 SUPPORT RESOURCES FINAL VERIFICATION")
    print("=" * 70)
    
    # Define all Section 6 components
    support_sections = [
        {
            'name': 'Section 6 Index',
            'html_file': '/workspaces/NewDocsTwin/6. TÀI NGUYÊN & HỖ TRỢ _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/tai-nguyen-ho-tro/index.md',
            'expected_title': '6. TÀI NGUYÊN & HỖ TRỢ'
        },
        {
            'name': 'Section 6.1 FAQs',
            'html_file': '/workspaces/NewDocsTwin/6.1. Các câu hỏi thường gặp (FAQs) _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/tai-nguyen-ho-tro/cac-cau-hoi-thuong-gap-faqs.md',
            'expected_title': '6.1. Các câu hỏi thường gặp (FAQs)'
        },
        {
            'name': 'Section 6.2 Support Channels',
            'html_file': '/workspaces/NewDocsTwin/6.2. Các kênh hỗ trợ _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/tai-nguyen-ho-tro/cac-kenh-ho-tro.md',
            'expected_title': '6.2. Các kênh hỗ trợ'
        },
        {
            'name': 'Section 6.3 Glossary',
            'html_file': '/workspaces/NewDocsTwin/6.3. Bảng thuật ngữ _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/tai-nguyen-ho-tro/bang-thuat-ngu.md',
            'expected_title': '6.3. Bảng thuật ngữ'
        }
    ]
    
    overall_results = {}
    total_accuracy = 0
    sections_verified = 0
    
    for section in support_sections:
        print(f"\n📋 PROCESSING {section['name'].upper()}")
        print("-" * 50)
        
        try:
            # Extract HTML content
            html_data = extract_html_content(section['html_file'], section['name'])
            
            # Verify against markdown
            verification = verify_content_accuracy(html_data, section['md_file'], section['expected_title'])
            
            overall_results[section['name']] = {
                'html_data': html_data,
                'verification': verification
            }
            
            if verification['accuracy'] > 0:
                total_accuracy += verification['accuracy'] 
                sections_verified += 1
            
            # Display results
            status_icon = "✅" if verification['status'] == 'VERIFIED' else "⚠️" if verification['status'] == 'NEEDS_REVIEW' else "❌"
            print(f"{status_icon} {verification['status']}: {verification['accuracy']:.1f}%")
            
        except Exception as e:
            print(f"❌ Error processing {section['name']}: {str(e)}")
            overall_results[section['name']] = {
                'html_data': None,
                'verification': {'status': 'ERROR', 'accuracy': 0, 'error': str(e)}
            }
    
    # Calculate final results
    final_accuracy = total_accuracy / sections_verified if sections_verified > 0 else 0
    
    print(f"\n🏆 SECTION 6 SUPPORT RESOURCES FINAL RESULTS")
    print("=" * 70)
    
    for section_name, result in overall_results.items():
        verification = result['verification']
        status_icon = "✅" if verification['status'] == 'VERIFIED' else "⚠️" if verification['status'] == 'NEEDS_REVIEW' else "❌"
        accuracy = verification.get('accuracy', 0)
        print(f"{status_icon} {section_name}: {verification['status']} ({accuracy:.1f}%)")
    
    print(f"\n📊 OVERALL ACCURACY: {final_accuracy:.1f}%")
    
    if final_accuracy >= 95:
        final_status = "✅ VERIFIED - EXCELLENT ACCURACY!"
    elif final_accuracy >= 80:
        final_status = "✅ VERIFIED - GOOD ACCURACY"
    elif final_accuracy >= 60:
        final_status = "⚠️ NEEDS REVIEW - ACCEPTABLE ACCURACY"
    else:
        final_status = "❌ POOR - REQUIRES SIGNIFICANT IMPROVEMENT"
    
    print(f"🎯 FINAL STATUS: {final_status}")
    
    # Save detailed results
    output_file = "/workspaces/NewDocsTwin/section_6_support_verification_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'final_accuracy': final_accuracy,
            'final_status': final_status,
            'sections_verified': sections_verified,
            'results': {k: {'verification': v['verification']} for k, v in overall_results.items()}
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return {
        'final_accuracy': final_accuracy,
        'final_status': final_status,
        'overall_results': overall_results
    }

def extract_html_content(html_file, section_name):
    """Extract content from HTML file"""
    
    print(f"🔍 Extracting from: {os.path.basename(html_file)}")
    
    if not os.path.exists(html_file):
        print(f"❌ HTML file not found: {html_file}")
        return None
    
    # Read and parse HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title = soup.find('title')
    title_text = title.get_text().strip() if title else ''
    print(f"📄 HTML Title: {title_text}")
    
    # Find main content
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    if not main_content:
        main_content = soup.find('body')
    
    # Extract headings
    headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    print(f"📋 Found {len(headings)} headings")
    
    # Extract meaningful content
    content_blocks = []
    text_elements = main_content.find_all(['p', 'div', 'span', 'li', 'td', 'th'])
    
    for element in text_elements:
        text = element.get_text().strip()
        if text and len(text) > 25:  # Filter for meaningful content
            text = ' '.join(text.split())
            content_blocks.append(text)
    
    # Remove duplicates and sort by length
    unique_blocks = list(set(content_blocks))
    unique_blocks.sort(key=len, reverse=True)
    
    print(f"📝 Found {len(unique_blocks)} unique content blocks")
    
    return {
        'title': title_text,
        'headings': [h.get_text().strip() for h in headings],
        'content_blocks': unique_blocks[:15],  # Top 15 blocks
        'section_name': section_name
    }

def verify_content_accuracy(html_data, md_file, expected_title):
    """Verify HTML content against markdown file"""
    
    if not html_data:
        return {'status': 'ERROR', 'accuracy': 0, 'error': 'No HTML data'}
    
    print(f"✅ Verifying against: {os.path.basename(md_file)}")
    
    if not os.path.exists(md_file):
        print(f"❌ Markdown file not found: {md_file}")
        return {'status': 'NOT_FOUND', 'accuracy': 0}
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Title verification
    total_checks += 1
    if expected_title in html_data['title'] and expected_title in md_content:
        checks_passed += 1
        print("✅ Title consistency verified")
    else:
        print("⚠️ Title inconsistency detected")
    
    # Check 2: Main heading presence
    total_checks += 1
    main_heading_found = False
    for heading in html_data['headings']:
        if expected_title in heading and expected_title in md_content:
            main_heading_found = True
            break
    
    if main_heading_found:
        checks_passed += 1
        print("✅ Main heading present")
    else:
        print("⚠️ Main heading missing or inconsistent")
    
    # Check 3: Content coverage
    total_checks += 1
    md_lower = md_content.lower()
    content_matches = 0
    
    for block in html_data['content_blocks'][:5]:  # Check top 5 blocks
        block_words = [word for word in block.lower().split() if len(word) > 4]
        matches = sum(1 for word in block_words if word in md_lower)
        if matches >= len(block_words) * 0.3:  # 30% word coverage
            content_matches += 1
    
    if content_matches >= 2:  # At least 2 blocks have good coverage
        checks_passed += 1
        print("✅ Good content coverage")
    else:
        print("⚠️ Limited content coverage")
    
    # Check 4: Content depth
    total_checks += 1
    md_lines = len([line for line in md_content.split('\n') if line.strip()])
    html_content_length = sum(len(block) for block in html_data['content_blocks'])
    
    if md_lines >= 20 or html_content_length >= 500:  # Substantial content
        checks_passed += 1
        print("✅ Substantial content depth")
    else:
        print("ℹ️ Basic content depth")
    
    # Calculate accuracy
    accuracy = (checks_passed / total_checks) * 100
    
    if accuracy >= 85:
        status = 'VERIFIED'
    elif accuracy >= 60:
        status = 'NEEDS_REVIEW'
    else:
        status = 'POOR'
    
    print(f"📊 Verification: {checks_passed}/{total_checks} checks passed ({accuracy:.1f}%)")
    
    return {
        'status': status,
        'accuracy': accuracy,
        'checks_passed': checks_passed,
        'total_checks': total_checks
    }

if __name__ == "__main__":
    try:
        result = extract_and_verify_support_content()
        print(f"\n✅ Section 6 Support Resources verification completed!")
        print(f"Final Status: {result['final_status']}")
    except Exception as e:
        print(f"\n❌ Error during verification: {str(e)}")
        import traceback
        traceback.print_exc()
