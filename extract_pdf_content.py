#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Content Extractor for Section 5 and Section 6
Extract accurate content from PDF files to update documentation
"""

import pdfplumber
import json
import re

def extract_pdf_content(pdf_path, section_name):
    """Extract text content from PDF file"""
    
    print(f"🔍 EXTRACTING {section_name} FROM PDF")
    print("=" * 60)
    print(f"📄 File: {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"📊 Total pages: {len(pdf.pages)}")
            
            all_text = ""
            page_contents = []
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n\n"
                    page_contents.append({
                        'page_number': i + 1,
                        'text': page_text.strip(),
                        'length': len(page_text.strip())
                    })
                    print(f"📄 Page {i+1}: {len(page_text.strip())} characters")
            
            # Clean and structure the text
            lines = all_text.split('\n')
            cleaned_lines = []
            
            for line in lines:
                line = line.strip()
                if line and len(line) > 3:  # Filter out very short lines
                    cleaned_lines.append(line)
            
            print(f"📝 Total text lines: {len(cleaned_lines)}")
            print(f"📏 Total characters: {len(all_text)}")
            
            # Extract headings (lines that might be headings)
            headings = []
            for line in cleaned_lines:
                # Look for potential headings (numbered sections, capitalized, etc.)
                if (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or
                    line.isupper() and len(line) < 100 or
                    line.startswith('#') or
                    (len(line) < 80 and not line.endswith('.') and not line.endswith(','))):
                    headings.append(line)
            
            print(f"🎯 Potential headings found: {len(headings)}")
            for i, heading in enumerate(headings[:10]):  # Show first 10
                print(f"  [{i+1}] {heading}")
            
            return {
                'section_name': section_name,
                'total_pages': len(pdf.pages),
                'all_text': all_text,
                'cleaned_lines': cleaned_lines,
                'headings': headings,
                'page_contents': page_contents
            }
            
    except Exception as e:
        print(f"❌ Error extracting PDF: {str(e)}")
        return None

def save_pdf_content(content, output_file):
    """Save extracted content to JSON file"""
    
    if not content:
        print("❌ No content to save")
        return
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Content saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error saving content: {str(e)}")

def main():
    """Main function to extract content from both PDF files"""
    
    print("🔍 PDF CONTENT EXTRACTION FOR SECTIONS 5 & 6")
    print("=" * 70)
    
    # Extract Section 5
    section5_content = extract_pdf_content("/workspaces/NewDocsTwin/Section 5.pdf", "Section 5 - API Documentation")
    if section5_content:
        save_pdf_content(section5_content, "/workspaces/NewDocsTwin/section_5_pdf_content.json")
    
    print("\n" + "="*70 + "\n")
    
    # Extract Section 6  
    section6_content = extract_pdf_content("/workspaces/NewDocsTwin/Section 6.pdf", "Section 6 - Support Resources")
    if section6_content:
        save_pdf_content(section6_content, "/workspaces/NewDocsTwin/section_6_pdf_content.json")
    
    print(f"\n🎉 PDF EXTRACTION COMPLETED!")
    print(f"✅ Section 5: {'Success' if section5_content else 'Failed'}")
    print(f"✅ Section 6: {'Success' if section6_content else 'Failed'}")
    
    return section5_content, section6_content

if __name__ == "__main__":
    try:
        section5, section6 = main()
    except Exception as e:
        print(f"\n❌ Error during PDF extraction: {str(e)}")
        import traceback
        traceback.print_exc()
