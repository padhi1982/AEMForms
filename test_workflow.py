#!/usr/bin/env python3
"""
Test the complete workflow with LPM27474.pdf
"""
import os
import sys
import json

os.chdir('/Users/hargovindpadhi/Tools/PDF-AEMforms')

# Test Agent 1: Parser
print("=" * 60)
print("🧪 Testing Agent 1: Parser (PDF → JSON)")
print("=" * 60)

try:
    from agent_parser import parse_pdf
    
    pdf_file = 'LPM27474.pdf'
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file not found: {pdf_file}")
        sys.exit(1)
    
    print(f"\n📄 Processing: {pdf_file}")
    form_data = parse_pdf(pdf_file)
    
    print("\n✅ Parser Result:")
    print(f"   Title: {form_data.get('formTitle', 'Unknown')}")
    print(f"   Description: {form_data.get('formDescription', 'N/A')}")
    print(f"   Fields found: {len(form_data.get('fields', []))}")
    
    # Save JSON
    json_file = 'test_headless_form.json'
    with open(json_file, 'w') as f:
        json.dump(form_data, f, indent=2)
    print(f"   Saved to: {json_file}")
    
    # Show first few fields
    print("\n   Sample Fields:")
    for field in form_data.get('fields', [])[:3]:
        print(f"     - {field.get('label')}: {field.get('type')}")
    
except Exception as e:
    print(f"❌ Parser Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ Workflow test completed successfully!")
print("=" * 60)
print("\nYou can now upload the PDF through the web interface:")
print("  http://localhost:5000")
