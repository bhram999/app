#!/usr/bin/env python3
"""
Test DMARC Parser with local XML files
This allows you to test the parser without connecting to Gmail
"""

import sys
import os
from dmarc_parser import DMARCParser

def test_local_xml(xml_file):
    """Test parser with a local XML file"""
    
    print("="*80)
    print("DMARC Parser - Local XML Test")
    print("="*80)
    print(f"\nTesting with file: {xml_file}\n")
    
    if not os.path.exists(xml_file):
        print(f"Error: File not found: {xml_file}")
        return False
    
    # Create parser instance (no email connection needed for this test)
    parser = DMARCParser("test@example.com", "dummy_password")
    
    # Read XML file
    with open(xml_file, 'rb') as f:
        xml_content = f.read()
    
    # Parse the XML
    parser.analyze_xml(xml_content, os.path.basename(xml_file), "test@example.com", "Test Report")
    
    # Generate report
    parser.generate_report()
    
    # Export to JSON
    output_file = xml_file.replace('.xml', '_result.json')
    parser.export_to_json(output_file)
    
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
    else:
        xml_file = 'sample_dmarc_report.xml'
    
    test_local_xml(xml_file)
