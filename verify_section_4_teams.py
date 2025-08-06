#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 4 Teams Content Verification
Compare extracted HTML content with current teams/index.md
"""

import json

def verify_section_4_content():
    """Verify Section 4 Teams content accuracy"""
    
    print("🔍 SECTION 4 TEAMS CONTENT VERIFICATION")
    print("=" * 60)
    
    # Load extracted content
    with open("/workspaces/NewDocsTwin/section_4_extracted_content.json", 'r', encoding='utf-8') as f:
        extracted = json.load(f)
    
    # Read current teams/index.md
    with open("/workspaces/NewDocsTwin/docs/teams/index.md", 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    print("📊 EXTRACTED HTML CONTENT:")
    print("-" * 40)
    print(f"Title: {extracted['title']}")
    print(f"Headings: {len(extracted['headings'])}")
    print(f"Content blocks: {len(extracted['content_blocks'])}")
    print(f"Teams-specific blocks: {len(extracted['teams_content'])}")
    
    print("\n🎯 CORE EXTRACTED CONTENT:")
    print("-" * 40)
    
    # Show core content from HTML
    main_content = None
    for block in extracted['content_blocks']:
        if len(block['text']) > 200 and 'sức mạnh' in block['text'].lower():
            main_content = block['text']
            break
    
    if main_content:
        print("Main intro paragraph:")
        print(f"'{main_content}'")
    
    # Show extracted sections
    print("\n📋 EXTRACTED SECTIONS:")
    print("-" * 40)
    
    sections = {}
    for block in extracted['teams_content']:
        text = block['text']
        if 'quản lý đội ngũ' in text.lower() and len(text) < 200:
            sections['team_management'] = text
        elif 'cộng tác trong' in text.lower() and len(text) < 200:
            sections['project_collaboration'] = text
        elif 'lưu ý:' in text.lower() and 'pro' in text.lower():
            sections['note'] = text
    
    for key, value in sections.items():
        print(f"{key}: {value}")
    
    print("\n📝 CURRENT TEAMS/INDEX.MD CONTENT:")
    print("-" * 40)
    
    # Extract key parts from current content
    lines = current_content.split('\n')
    
    current_intro = None
    current_note = None
    current_sections = {}
    
    for i, line in enumerate(lines):
        if 'Sức mạnh của Twin AI' in line:
            # Get the full intro paragraph
            current_intro = line
            if i + 1 < len(lines):
                current_intro += " " + lines[i + 1]
        elif 'Lưu ý:' in line and 'Pro' in line:
            current_note = line
        elif '4.1. Quản lý Đội ngũ' in line:
            if i + 2 < len(lines):
                current_sections['team_management'] = lines[i + 2]
        elif '4.2. Cộng tác trong' in line:
            if i + 2 < len(lines):
                current_sections['project_collaboration'] = lines[i + 2]
    
    print(f"Current intro: {current_intro}")
    print(f"Current note: {current_note}")
    print(f"Current sections: {current_sections}")
    
    print("\n🔍 ACCURACY VERIFICATION:")
    print("-" * 40)
    
    accuracy_score = 0
    total_checks = 0
    
    # Check 1: Title
    total_checks += 1
    if extracted['title'] == "4. QUẢN LÝ TEAMS CỦA BẠN | Twin AI Docs":
        print("✅ Title matches")
        accuracy_score += 1
    else:
        print("❌ Title mismatch")
    
    # Check 2: Main intro paragraph
    total_checks += 1
    if main_content and current_intro:
        # Compare core message
        html_core = main_content[:200].lower()
        current_core = current_intro[:200].lower()
        if 'sức mạnh' in html_core and 'sức mạnh' in current_core and 'cộng tác' in html_core and 'cộng tác' in current_core:
            print("✅ Intro paragraph core message matches")
            accuracy_score += 1
        else:
            print("❌ Intro paragraph mismatch")
            print(f"  HTML: {html_core}")
            print(f"  Current: {current_core}")
    
    # Check 3: Pro note
    total_checks += 1
    if sections.get('note') and current_note:
        if 'pro' in sections['note'].lower() and 'pro' in current_note.lower():
            print("✅ Pro tier note matches")
            accuracy_score += 1
        else:
            print("❌ Pro tier note mismatch")
    
    # Check 4: Section descriptions
    total_checks += 1
    html_team_mgmt = sections.get('team_management', '').lower()
    current_team_mgmt = current_sections.get('team_management', '').lower()
    
    if 'mời' in html_team_mgmt and 'mời' in current_team_mgmt:
        print("✅ Team management description matches")
        accuracy_score += 1
    else:
        print("❌ Team management description mismatch")
    
    total_checks += 1
    html_proj_collab = sections.get('project_collaboration', '').lower()
    current_proj_collab = current_sections.get('project_collaboration', '').lower()
    
    if 'chia sẻ' in html_proj_collab and 'chia sẻ' in current_proj_collab:
        print("✅ Project collaboration description matches")
        accuracy_score += 1
    else:
        print("❌ Project collaboration description mismatch")
    
    # Calculate accuracy
    accuracy_percentage = (accuracy_score / total_checks) * 100
    
    print(f"\n📊 ACCURACY SCORE: {accuracy_score}/{total_checks} ({accuracy_percentage:.1f}%)")
    
    if accuracy_percentage >= 95:
        print("🎉 EXCELLENT: Content accuracy is very high!")
        status = "VERIFIED"
    elif accuracy_percentage >= 80:
        print("✅ GOOD: Content accuracy is acceptable")
        status = "MOSTLY_ACCURATE"
    else:
        print("⚠️ NEEDS IMPROVEMENT: Content accuracy is below standard")
        status = "NEEDS_REVIEW"
    
    print(f"\n🏆 FINAL STATUS: {status}")
    
    return {
        'status': status,
        'accuracy': accuracy_percentage,
        'checks_passed': accuracy_score,
        'total_checks': total_checks
    }

if __name__ == "__main__":
    try:
        result = verify_section_4_content()
        print(f"\n✅ Section 4 Teams verification completed: {result['status']}")
    except Exception as e:
        print(f"\n❌ Error during verification: {str(e)}")
        import traceback
        traceback.print_exc()
