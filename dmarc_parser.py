#!/usr/bin/env python3
"""
DMARC Report Parser - Fetch and analyze DMARC aggregate reports from Gmail

This script connects to Gmail via IMAP, fetches DMARC aggregate reports (XML),
parses them, and identifies authentication failures (DKIM, SPF, DMARC alignment).
"""

import imaplib
import email
from email.header import decode_header
import xml.etree.ElementTree as ET
import gzip
import zipfile
import io
import os
import json
import argparse
from datetime import datetime
from collections import defaultdict
import base64
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class DMARCParser:
    def __init__(self, email_address, password, imap_server='imap.gmail.com', verbose=False):
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.reports = []
        self.failures = []
        self.verbose = verbose
        
    def connect(self):
        """Connect to Gmail IMAP server"""
        try:
            print(f"{Colors.CYAN}Connecting to {self.imap_server}...{Colors.END}")
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)
            print(f"{Colors.GREEN}✓ Connected successfully{Colors.END}\n")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ Connection failed: {str(e)}{Colors.END}")
            return False
    
    def fetch_dmarc_reports(self, mailbox='INBOX', limit=50):
        """Fetch DMARC report emails"""
        try:
            self.mail.select(mailbox)
            
            # Search for DMARC reports with multiple criteria
            # Standard DMARC report subject format: "Report Domain: example.com Submitter: reporter.com"
            search_criteria = [
                'SUBJECT "Report Domain:"',  # Standard DMARC report format
                'FROM "dmarc"',               # From addresses containing dmarc
                'SUBJECT "dmarc"',            # Subject containing dmarc
                'FROM "noreply@google.com"',  # Google DMARC reports
                'FROM "yahoo"',               # Yahoo DMARC reports
                'FROM "postmaster"',          # Generic postmaster reports
            ]
            
            email_ids = []
            for criteria in search_criteria:
                status, messages = self.mail.search(None, criteria)
                if status == 'OK' and messages[0]:
                    found = messages[0].split()
                    email_ids.extend(found)
                    if self.verbose and found:
                        print(f"{Colors.CYAN}  Criteria '{criteria}': found {len(found)} emails{Colors.END}")
            
            # Remove duplicates and limit
            unique_ids = list(set(email_ids))
            email_ids = unique_ids[-limit:]
            
            if self.verbose:
                print(f"{Colors.CYAN}Total unique emails: {len(unique_ids)}, processing last {len(email_ids)}{Colors.END}")
            
            print(f"{Colors.BLUE}Found {len(email_ids)} potential DMARC report emails{Colors.END}\n")
            
            for email_id in email_ids:
                self.process_email(email_id)
                
        except Exception as e:
            print(f"{Colors.RED}Error fetching emails: {str(e)}{Colors.END}")
    
    def process_email(self, email_id):
        """Process individual email and extract XML attachments"""
        try:
            status, msg_data = self.mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                return
            
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            subject = self.decode_header_value(email_message['Subject'])
            from_addr = email_message['From']
            
            # Debug: Check if this looks like a DMARC report
            if 'Report Domain:' in subject or 'dmarc' in subject.lower() or 'aggregate' in subject.lower():
                found_attachment = False
                
                # Process attachments
                for part in email_message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    
                    filename = part.get_filename()
                    if filename:
                        # Check for DMARC report file extensions
                        if filename.endswith(('.xml', '.gz', '.zip')):
                            found_attachment = True
                            file_data = part.get_payload(decode=True)
                            if file_data:
                                self.parse_dmarc_xml(file_data, filename, from_addr, subject)
                
                if not found_attachment:
                    print(f"{Colors.YELLOW}Note: Email with subject '{subject[:50]}...' has no XML/GZ/ZIP attachment{Colors.END}")
                    
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Could not process email {email_id}: {str(e)}{Colors.END}")
    
    def decode_header_value(self, value):
        """Decode email header value"""
        if value is None:
            return ""
        decoded = decode_header(value)
        header_text = ""
        for text, encoding in decoded:
            if isinstance(text, bytes):
                header_text += text.decode(encoding or 'utf-8')
            else:
                header_text += text
        return header_text
    
    def parse_dmarc_xml(self, file_data, filename, from_addr, subject):
        """Parse DMARC XML from attachment"""
        try:
            xml_content = None
            
            # Handle compressed files
            if filename.endswith('.gz'):
                xml_content = gzip.decompress(file_data)
            elif filename.endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(file_data)) as zf:
                    # Get first XML file in zip
                    for name in zf.namelist():
                        if name.endswith('.xml'):
                            xml_content = zf.read(name)
                            break
            elif filename.endswith('.xml'):
                xml_content = file_data
            else:
                return
            
            if xml_content:
                self.analyze_xml(xml_content, filename, from_addr, subject)
                
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Could not parse {filename}: {str(e)}{Colors.END}")
    
    def analyze_xml(self, xml_content, filename, from_addr, subject):
        """Analyze DMARC XML report"""
        try:
            root = ET.fromstring(xml_content)
            
            # Extract metadata
            report_metadata = root.find('report_metadata')
            org_name = report_metadata.find('org_name').text if report_metadata.find('org_name') is not None else 'Unknown'
            report_id = report_metadata.find('report_id').text if report_metadata.find('report_id') is not None else 'Unknown'
            
            date_range = report_metadata.find('date_range')
            date_begin = datetime.fromtimestamp(int(date_range.find('begin').text))
            date_end = datetime.fromtimestamp(int(date_range.find('end').text))
            
            # Extract policy
            policy_published = root.find('policy_published')
            domain = policy_published.find('domain').text
            dmarc_policy = policy_published.find('p').text
            
            report_info = {
                'filename': filename,
                'org_name': org_name,
                'report_id': report_id,
                'domain': domain,
                'date_begin': date_begin.strftime('%Y-%m-%d %H:%M:%S'),
                'date_end': date_end.strftime('%Y-%m-%d %H:%M:%S'),
                'dmarc_policy': dmarc_policy,
                'records': []
            }
            
            # Process records
            has_failures = False
            for record in root.findall('record'):
                record_data = self.parse_record(record)
                report_info['records'].append(record_data)
                
                if record_data['has_failure']:
                    has_failures = True
                    self.failures.append({
                        'domain': domain,
                        'org_name': org_name,
                        'report_id': report_id,
                        'date': date_begin.strftime('%Y-%m-%d'),
                        **record_data
                    })
            
            self.reports.append(report_info)
            
            if has_failures:
                print(f"{Colors.RED}⚠ FAILURES FOUND{Colors.END} in report from {Colors.BOLD}{org_name}{Colors.END} for domain {Colors.BOLD}{domain}{Colors.END}")
            else:
                print(f"{Colors.GREEN}✓ All passed{Colors.END} in report from {org_name} for {domain}")
                
        except Exception as e:
            print(f"{Colors.RED}Error analyzing XML: {str(e)}{Colors.END}")
    
    def parse_record(self, record):
        """Parse individual DMARC record"""
        row = record.find('row')
        source_ip = row.find('source_ip').text
        count = int(row.find('count').text)
        
        policy_evaluated = row.find('policy_evaluated')
        disposition = policy_evaluated.find('disposition').text
        dkim_result = policy_evaluated.find('dkim').text
        spf_result = policy_evaluated.find('spf').text
        
        # Get authentication results
        auth_results = record.find('auth_results')
        
        dkim_details = []
        if auth_results.find('dkim') is not None:
            for dkim in auth_results.findall('dkim'):
                dkim_domain = dkim.find('domain').text if dkim.find('domain') is not None else 'N/A'
                dkim_auth_result = dkim.find('result').text if dkim.find('result') is not None else 'none'
                dkim_details.append({'domain': dkim_domain, 'result': dkim_auth_result})
        
        spf_details = []
        if auth_results.find('spf') is not None:
            for spf in auth_results.findall('spf'):
                spf_domain = spf.find('domain').text if spf.find('domain') is not None else 'N/A'
                spf_auth_result = spf.find('result').text if spf.find('result') is not None else 'none'
                spf_details.append({'domain': spf_domain, 'result': spf_auth_result})
        
        # Determine if there are failures
        has_failure = (dkim_result != 'pass' or spf_result != 'pass')
        
        # Get identifiers
        identifiers = record.find('identifiers')
        header_from = identifiers.find('header_from').text if identifiers.find('header_from') is not None else 'N/A'
        
        return {
            'source_ip': source_ip,
            'count': count,
            'disposition': disposition,
            'dkim_result': dkim_result,
            'spf_result': spf_result,
            'dkim_details': dkim_details,
            'spf_details': spf_details,
            'header_from': header_from,
            'has_failure': has_failure
        }
    
    def generate_report(self):
        """Generate detailed failure report"""
        if not self.failures:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 No DMARC failures found! All authentication checks passed.{Colors.END}\n")
            return
        
        print(f"\n{Colors.RED}{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}DMARC AUTHENTICATION FAILURES REPORT{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}{'='*80}{Colors.END}\n")
        
        # Group failures by domain
        failures_by_domain = defaultdict(list)
        for failure in self.failures:
            failures_by_domain[failure['domain']].append(failure)
        
        for domain, failures in failures_by_domain.items():
            print(f"{Colors.CYAN}{Colors.BOLD}Domain: {domain}{Colors.END}")
            print(f"{Colors.CYAN}{'─'*80}{Colors.END}")
            
            total_failed_count = sum(f['count'] for f in failures)
            print(f"Total failed messages: {Colors.RED}{Colors.BOLD}{total_failed_count}{Colors.END}\n")
            
            for idx, failure in enumerate(failures, 1):
                print(f"{Colors.YELLOW}Failure #{idx}:{Colors.END}")
                print(f"  Source IP: {failure['source_ip']}")
                print(f"  Count: {failure['count']} messages")
                print(f"  Header From: {failure['header_from']}")
                print(f"  Date: {failure['date']}")
                print(f"  Reporter: {failure['org_name']}")
                
                # DKIM Status
                if failure['dkim_result'] != 'pass':
                    print(f"  {Colors.RED}✗ DKIM: {failure['dkim_result'].upper()}{Colors.END}")
                    if failure['dkim_details']:
                        for dkim in failure['dkim_details']:
                            print(f"    - Domain: {dkim['domain']}, Result: {dkim['result']}")
                else:
                    print(f"  {Colors.GREEN}✓ DKIM: PASS{Colors.END}")
                
                # SPF Status
                if failure['spf_result'] != 'pass':
                    print(f"  {Colors.RED}✗ SPF: {failure['spf_result'].upper()}{Colors.END}")
                    if failure['spf_details']:
                        for spf in failure['spf_details']:
                            print(f"    - Domain: {spf['domain']}, Result: {spf['result']}")
                else:
                    print(f"  {Colors.GREEN}✓ SPF: PASS{Colors.END}")
                
                print(f"  Disposition: {failure['disposition']}")
                
                # Recommendations
                print(f"\n  {Colors.MAGENTA}Recommendations:{Colors.END}")
                self.print_recommendations(failure)
                print()
            
            print()
        
        # Summary
        print(f"{Colors.BOLD}SUMMARY:{Colors.END}")
        print(f"Total reports analyzed: {len(self.reports)}")
        print(f"Reports with failures: {len(failures_by_domain)}")
        print(f"Total failure records: {len(self.failures)}")
        print(f"Total failed messages: {sum(f['count'] for f in self.failures)}")
    
    def print_recommendations(self, failure):
        """Print specific recommendations based on failure type"""
        recommendations = []
        
        if failure['dkim_result'] != 'pass':
            recommendations.append("DKIM Failure:")
            recommendations.append("  • Verify DKIM signing is enabled on your mail server")
            recommendations.append("  • Check DKIM private key configuration")
            recommendations.append("  • Ensure DKIM DNS record is published correctly")
            recommendations.append("  • Verify selector and domain match in email headers")
        
        if failure['spf_result'] != 'pass':
            recommendations.append("SPF Failure:")
            recommendations.append(f"  • Add IP {failure['source_ip']} to SPF record if legitimate")
            recommendations.append("  • Review SPF record for missing authorized servers")
            recommendations.append("  • Check for SPF record syntax errors")
            recommendations.append("  • Ensure SPF record is not exceeding DNS lookup limit (10)")
        
        if failure['disposition'] == 'reject':
            recommendations.append("CRITICAL: Messages are being REJECTED!")
            recommendations.append("  • Immediate action required to prevent email delivery issues")
        elif failure['disposition'] == 'quarantine':
            recommendations.append("WARNING: Messages are being QUARANTINED (likely spam folder)")
        
        # IP reputation
        recommendations.append("General recommendations:")
        recommendations.append(f"  • Check IP reputation for {failure['source_ip']}")
        recommendations.append("  • Verify this IP is authorized to send on your behalf")
        recommendations.append("  • Use DMARC alignment to ensure domain consistency")
        
        for rec in recommendations:
            print(f"    {rec}")
    
    def export_to_json(self, filepath='dmarc_failures.json'):
        """Export failures to JSON file"""
        output = {
            'generated_at': datetime.now().isoformat(),
            'total_reports': len(self.reports),
            'total_failures': len(self.failures),
            'failures': self.failures,
            'all_reports': self.reports
        }
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n{Colors.GREEN}✓ Full report exported to: {filepath}{Colors.END}")
    
    def disconnect(self):
        """Disconnect from IMAP server"""
        try:
            self.mail.close()
            self.mail.logout()
        except:
            pass


def main():
    parser = argparse.ArgumentParser(
        description='DMARC Report Parser - Analyze email authentication failures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dmarc_parser.py --email user@gmail.com --password "your_app_password"
  python dmarc_parser.py --email user@gmail.com --password "your_password" --limit 100
  python dmarc_parser.py --email user@gmail.com --password "your_password" --output my_report.json

Note: For Gmail, use an App Password instead of your regular password.
Generate one at: https://myaccount.google.com/apppasswords
        """
    )
    
    parser.add_argument('--email', required=True, help='Gmail email address')
    parser.add_argument('--password', required=True, help='Gmail password or App Password')
    parser.add_argument('--mailbox', default='INBOX', help='Mailbox to search (default: INBOX)')
    parser.add_argument('--limit', type=int, default=50, help='Maximum number of emails to process (default: 50)')
    parser.add_argument('--output', default='dmarc_failures.json', help='Output JSON file path')
    parser.add_argument('--server', default='imap.gmail.com', help='IMAP server (default: imap.gmail.com)')
    
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║           DMARC REPORT PARSER & ANALYZER                 ║")
    print("║        Email Authentication Failure Detection            ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    parser_obj = DMARCParser(args.email, args.password, args.server)
    
    if not parser_obj.connect():
        sys.exit(1)
    
    try:
        parser_obj.fetch_dmarc_reports(args.mailbox, args.limit)
        parser_obj.generate_report()
        parser_obj.export_to_json(args.output)
    finally:
        parser_obj.disconnect()
    
    print(f"\n{Colors.GREEN}Done!{Colors.END}\n")


if __name__ == '__main__':
    main()
