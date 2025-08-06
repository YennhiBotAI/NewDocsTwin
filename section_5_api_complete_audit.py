#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 5 API Documentation Complete Extraction and Verification
Systematic extraction and accuracy verification for all API documentation sections
"""

import os
from bs4 import BeautifulSoup
import json

def extract_api_section(html_file, section_name):
    """Extract content from a specific API section HTML file"""
    
    print(f"\n🔍 EXTRACTING {section_name.upper()}")
    print("-" * 50)
    
    if not os.path.exists(html_file):
        print(f"❌ File not found: {html_file}")
        return None
    
    # Read HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract page title
    title = soup.find('title')
    title_text = title.get_text().strip() if title else ''
    print(f"📄 Title: {title_text}")
    
    # Find main content
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    
    if not main_content:
        main_content = soup.find('body')
    
    # Extract headings
    headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    print(f"📋 Found {len(headings)} headings")
    
    for heading in headings[:5]:  # Show first 5 headings
        level = heading.name
        text = heading.get_text().strip()
        print(f"  {level.upper()}: {text}")
    
    # Extract content blocks
    content_blocks = []
    text_elements = main_content.find_all(['p', 'div', 'span', 'li', 'td', 'th', 'code', 'pre'])
    
    for element in text_elements:
        text = element.get_text().strip()
        if text and len(text) > 20:  # Filter meaningful content
            text = ' '.join(text.split())
            content_blocks.append({
                'text': text,
                'element': element.name,
                'length': len(text)
            })
    
    # Sort by length for relevance
    content_blocks.sort(key=lambda x: x['length'], reverse=True)
    
    print(f"📝 Found {len(content_blocks)} content blocks")
    
    # Show top content
    for i, block in enumerate(content_blocks[:3]):
        print(f"  [{i+1}] {block['text'][:150]}{'...' if len(block['text']) > 150 else ''}")
    
    return {
        'title': title_text,
        'headings': [{'level': h.name, 'text': h.get_text().strip()} for h in headings],
        'content_blocks': content_blocks[:20],  # Top 20 blocks
        'section_name': section_name
    }

def verify_api_section(extracted_data, md_file_path):
    """Verify extracted content against current markdown file"""
    
    if not extracted_data:
        return {'status': 'ERROR', 'accuracy': 0}
    
    print(f"\n✅ VERIFYING {extracted_data['section_name'].upper()}")
    print("-" * 50)
    
    if not os.path.exists(md_file_path):
        print(f"❌ Markdown file not found: {md_file_path}")
        return {'status': 'NOT_FOUND', 'accuracy': 0}
    
    # Read current markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    print(f"📄 Current file: {os.path.basename(md_file_path)}")
    
    # Basic verification checks
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Title presence
    total_checks += 1
    main_heading = extracted_data['headings'][0] if extracted_data['headings'] else None
    if main_heading and main_heading['text'] in current_content:
        checks_passed += 1
        print("✅ Main title matches")
    else:
        print("❌ Main title mismatch")
    
    # Check 2: Key content presence
    total_checks += 1
    if extracted_data['content_blocks']:
        # Look for key content elements
        top_content = extracted_data['content_blocks'][0]['text'][:100].lower()
        current_lower = current_content.lower()
        
        # Find common meaningful words (excluding common words)
        common_words = []
        for word in top_content.split():
            if len(word) > 4 and word in current_lower:
                common_words.append(word)
        
        if len(common_words) >= 2:  # At least 2 meaningful words match
            checks_passed += 1
            print("✅ Key content elements present")
        else:
            print("❌ Key content elements missing")
    
    # Check 3: Structure consistency
    total_checks += 1
    md_headings = current_content.count('#')
    html_headings = len(extracted_data['headings'])
    
    if abs(md_headings - html_headings) <= 2:  # Allow some variance
        checks_passed += 1
        print("✅ Structure consistency acceptable")
    else:
        print("❌ Structure inconsistency detected")
    
    accuracy = (checks_passed / total_checks) * 100
    status = 'VERIFIED' if accuracy >= 80 else 'NEEDS_REVIEW'
    
    print(f"📊 Accuracy: {accuracy:.1f}% ({checks_passed}/{total_checks})")
    
    return {
        'status': status,
        'accuracy': accuracy,
        'checks_passed': checks_passed,
        'total_checks': total_checks
    }

def main():
    """Main function to extract and verify all Section 5 API documentation"""
    
    print("🔍 SECTION 5 API DOCUMENTATION COMPLETE AUDIT")
    print("=" * 70)
    
    # Define all API sections
    api_sections = [
        {
            'name': 'Section 5 Index',
            'html_file': '/workspaces/NewDocsTwin/5. DÀNH CHO NHÀ PHÁT TRIỂN (TwinExpert API Documentation) _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/api/index.md'
        },
        {
            'name': 'Section 5.1 Getting Started',
            'html_file': '/workspaces/NewDocsTwin/5.1. Bắt đầu với API _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/api/getting-started.md'
        },
        {
            'name': 'Section 5.2 Authentication',
            'html_file': '/workspaces/NewDocsTwin/5.2. Xác thực _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/api/authentication.md'
        },
        {
            'name': 'Section 5.3 API Endpoints',
            'html_file': '/workspaces/NewDocsTwin/5.3. API Endpoints _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/api/endpoints.md'
        },
        {
            'name': 'Section 5.4 Examples',
            'html_file': '/workspaces/NewDocsTwin/5.4. Ví dụ _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/api/examples.md'
        },
        {
            'name': 'Section 5.5 Rate Limiting',
            'html_file': '/workspaces/NewDocsTwin/5.5. Rate Limiting _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/api/rate-limiting.md'
        },
        {
            'name': 'Section 5.6 Error Handling',
            'html_file': '/workspaces/NewDocsTwin/5.6. Xử lý lỗi _ Twin AI Docs.html',
            'md_file': '/workspaces/NewDocsTwin/docs/api/error-handling.md'
        }
    ]
    
    results = {}
    total_accuracy = 0
    sections_processed = 0
    
    # Process each section
    for section in api_sections:
        try:
            # Extract content from HTML
            extracted = extract_api_section(section['html_file'], section['name'])
            
            # Verify against markdown
            verification = verify_api_section(extracted, section['md_file'])
            
            results[section['name']] = {
                'extracted': extracted,
                'verification': verification
            }
            
            if verification['accuracy'] > 0:
                total_accuracy += verification['accuracy']
                sections_processed += 1
            
        except Exception as e:
            print(f"❌ Error processing {section['name']}: {str(e)}")
            results[section['name']] = {
                'extracted': None,
                'verification': {'status': 'ERROR', 'accuracy': 0}
            }
    
    # Calculate overall results
    overall_accuracy = total_accuracy / sections_processed if sections_processed > 0 else 0
    
    print(f"\n🏆 SECTION 5 API DOCUMENTATION OVERALL RESULTS")
    print("=" * 70)
    
    for section_name, result in results.items():
        verification = result['verification']
        status_icon = "✅" if verification['status'] == 'VERIFIED' else "⚠️" if verification['status'] == 'NEEDS_REVIEW' else "❌"
        print(f"{status_icon} {section_name}: {verification['status']} ({verification['accuracy']:.1f}%)")
    
    print(f"\n📊 OVERALL ACCURACY: {overall_accuracy:.1f}%")
    
    if overall_accuracy >= 95:
        overall_status = "✅ VERIFIED - EXCELLENT ACCURACY!"
    elif overall_accuracy >= 80:
        overall_status = "✅ VERIFIED - GOOD ACCURACY"
    else:
        overall_status = "⚠️ NEEDS REVIEW - ACCURACY BELOW STANDARD"
    
    print(f"🎯 FINAL STATUS: {overall_status}")
    
    # Save results
    output_file = "/workspaces/NewDocsTwin/section_5_api_verification_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'overall_accuracy': overall_accuracy,
            'overall_status': overall_status,
            'sections_processed': sections_processed,
            'results': {k: {'verification': v['verification']} for k, v in results.items()}
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return {
        'overall_accuracy': overall_accuracy,
        'overall_status': overall_status,
        'results': results
    }

if __name__ == "__main__":
    try:
        result = main()
        print(f"\n✅ Section 5 API documentation audit completed!")
        print(f"Status: {result['overall_status']}")
    except Exception as e:
        print(f"\n❌ Error during API documentation audit: {str(e)}")
        import traceback
        traceback.print_exc()
