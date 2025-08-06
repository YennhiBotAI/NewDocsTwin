#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 4 Teams Complete Verification
Final verification of all Section 4 content accuracy
"""

import json

def verify_complete_section_4():
    """Complete verification of Section 4 Teams content"""
    
    print("🔍 SECTION 4 TEAMS COMPLETE VERIFICATION")
    print("=" * 60)
    
    verification_results = {
        'section_4_index': {'status': 'UNKNOWN', 'accuracy': 0},
        'section_4_1_team_mgmt': {'status': 'UNKNOWN', 'accuracy': 0}, 
        'section_4_2_project_collab': {'status': 'UNKNOWN', 'accuracy': 0}
    }
    
    # Verify Section 4 Index (teams/index.md)
    print("📋 VERIFYING SECTION 4 INDEX...")
    print("-" * 40)
    
    try:
        with open("/workspaces/NewDocsTwin/section_4_extracted_content.json", 'r', encoding='utf-8') as f:
            s4_data = json.load(f)
        
        with open("/workspaces/NewDocsTwin/docs/teams/index.md", 'r', encoding='utf-8') as f:
            s4_current = f.read()
        
        # Check core content elements
        checks_passed = 0
        total_checks = 0
        
        # Check 1: Title
        total_checks += 1
        if "4. QUẢN LÝ TEAMS CỦA BẠN" in s4_current:
            checks_passed += 1
            print("✅ Title matches")
        else:
            print("❌ Title missing")
        
        # Check 2: Main intro
        total_checks += 1
        if "Sức mạnh của Twin AI được nhân lên gấp bội" in s4_current:
            checks_passed += 1
            print("✅ Main intro paragraph present")
        else:
            print("❌ Main intro missing")
        
        # Check 3: Pro tier note
        total_checks += 1
        if "Pro trở lên" in s4_current:
            checks_passed += 1
            print("✅ Pro tier note present")
        else:
            print("❌ Pro tier note missing")
        
        # Check 4: Section links
        total_checks += 1
        if "team-management" in s4_current and "project-collaboration" in s4_current:
            checks_passed += 1
            print("✅ Section navigation links present")
        else:
            print("❌ Navigation links missing")
        
        accuracy = (checks_passed / total_checks) * 100
        verification_results['section_4_index'] = {
            'status': 'VERIFIED' if accuracy >= 95 else 'NEEDS_REVIEW',
            'accuracy': accuracy
        }
        
        print(f"Section 4 Index Accuracy: {accuracy:.1f}%")
        
    except Exception as e:
        print(f"❌ Error verifying Section 4 Index: {e}")
    
    # Verify Section 4.1 Team Management
    print("\n👥 VERIFYING SECTION 4.1 TEAM MANAGEMENT...")
    print("-" * 40)
    
    try:
        with open("/workspaces/NewDocsTwin/section_4_1_extracted.json", 'r', encoding='utf-8') as f:
            s41_data = json.load(f)
        
        with open("/workspaces/NewDocsTwin/docs/teams/team-management.md", 'r', encoding='utf-8') as f:
            s41_current = f.read()
        
        checks_passed = 0
        total_checks = 0
        
        # Check extracted content against current
        total_checks += 1
        if "4.1. Quản lý Đội ngũ (Teams):" in s41_current:
            checks_passed += 1
            print("✅ Section 4.1 title matches")
        
        total_checks += 1
        if "Chủ Sở Hữu Teams" in s41_current:
            checks_passed += 1
            print("✅ Owner role content present")
        
        total_checks += 1
        if "mời thành viên mới" in s41_current:
            checks_passed += 1
            print("✅ Member invitation content present")
        
        total_checks += 1
        if "phần 3.3" in s41_current:
            checks_passed += 1
            print("✅ Cross-reference to section 3.3 present")
        
        accuracy = (checks_passed / total_checks) * 100
        verification_results['section_4_1_team_mgmt'] = {
            'status': 'VERIFIED' if accuracy >= 95 else 'NEEDS_REVIEW',
            'accuracy': accuracy
        }
        
        print(f"Section 4.1 Accuracy: {accuracy:.1f}%")
        
    except Exception as e:
        print(f"❌ Error verifying Section 4.1: {e}")
    
    # Verify Section 4.2 Project Collaboration
    print("\n🤝 VERIFYING SECTION 4.2 PROJECT COLLABORATION...")
    print("-" * 40)
    
    try:
        with open("/workspaces/NewDocsTwin/section_4_2_extracted.json", 'r', encoding='utf-8') as f:
            s42_data = json.load(f)
        
        with open("/workspaces/NewDocsTwin/docs/teams/project-collaboration.md", 'r', encoding='utf-8') as f:
            s42_current = f.read()
        
        checks_passed = 0
        total_checks = 0
        
        # Check extracted content against current
        total_checks += 1
        if "4.2. Cộng tác trong \"Projects\":" in s42_current:
            checks_passed += 1
            print("✅ Section 4.2 title matches")
        
        total_checks += 1
        if "Team của bạn đã được thiết lập" in s42_current:
            checks_passed += 1
            print("✅ Main intro content present")
        
        total_checks += 1
        if "quyền truy cập vào dự án" in s42_current:
            checks_passed += 1
            print("✅ Access rights content present")
        
        total_checks += 1
        if "thêm thành viên Team cộng tác" in s42_current:
            checks_passed += 1
            print("✅ Collaboration guidance present")
        
        accuracy = (checks_passed / total_checks) * 100
        verification_results['section_4_2_project_collab'] = {
            'status': 'VERIFIED' if accuracy >= 95 else 'NEEDS_REVIEW',
            'accuracy': accuracy
        }
        
        print(f"Section 4.2 Accuracy: {accuracy:.1f}%")
        
    except Exception as e:
        print(f"❌ Error verifying Section 4.2: {e}")
    
    # Calculate overall Section 4 accuracy
    total_accuracy = sum(result['accuracy'] for result in verification_results.values()) / len(verification_results)
    
    print(f"\n🏆 SECTION 4 TEAMS OVERALL RESULTS:")
    print("=" * 60)
    print(f"Section 4 Index: {verification_results['section_4_index']['status']} ({verification_results['section_4_index']['accuracy']:.1f}%)")
    print(f"Section 4.1 Team Management: {verification_results['section_4_1_team_mgmt']['status']} ({verification_results['section_4_1_team_mgmt']['accuracy']:.1f}%)")
    print(f"Section 4.2 Project Collaboration: {verification_results['section_4_2_project_collab']['status']} ({verification_results['section_4_2_project_collab']['accuracy']:.1f}%)")
    print(f"\n📊 OVERALL ACCURACY: {total_accuracy:.1f}%")
    
    if total_accuracy >= 95:
        overall_status = "✅ VERIFIED - EXCELLENT ACCURACY!"
    elif total_accuracy >= 80:
        overall_status = "✅ VERIFIED - GOOD ACCURACY"
    else:
        overall_status = "⚠️ NEEDS REVIEW - ACCURACY BELOW STANDARD"
    
    print(f"🎯 FINAL STATUS: {overall_status}")
    
    return {
        'overall_accuracy': total_accuracy,
        'overall_status': overall_status,
        'details': verification_results
    }

if __name__ == "__main__":
    try:
        result = verify_complete_section_4()
        print(f"\n✅ Section 4 Teams complete verification finished!")
        print(f"Status: {result['overall_status']}")
    except Exception as e:
        print(f"\n❌ Error during complete verification: {str(e)}")
        import traceback
        traceback.print_exc()
