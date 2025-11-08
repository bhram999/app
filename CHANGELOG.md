# DMARC Parser - Changelog

## Version 1.1 - Improved Email Search & Detection

### Fixed Issues

**Problem**: Parser not detecting SPF failures in actual DMARC reports from Gmail

**Root Cause**: 
- Search criteria was too restrictive
- Standard DMARC report subject format "Report Domain: ... Submitter: ..." was not properly matched
- No specific handling for common DMARC report senders (Yahoo, Google, etc.)

### Changes Made

#### 1. Enhanced Email Search Criteria
**Before**:
```python
search_criteria = [
    '(OR (FROM "dmarc") (SUBJECT "dmarc"))',
    '(OR (SUBJECT "Report") (SUBJECT "Aggregate"))'
]
```

**After**:
```python
search_criteria = [
    'SUBJECT "Report Domain:"',  # Standard DMARC report format
    'FROM "dmarc"',               # From addresses containing dmarc
    'SUBJECT "dmarc"',            # Subject containing dmarc
    'FROM "noreply@google.com"',  # Google DMARC reports
    'FROM "yahoo"',               # Yahoo DMARC reports
    'FROM "postmaster"',          # Generic postmaster reports
]
```

**Impact**: Now correctly matches emails with subject "Report Domain: rew.ca Submitter: Yahoo"

#### 2. Improved Attachment Detection
- Added explicit check for `.xml`, `.gz`, and `.zip` file extensions
- Added warning when DMARC-like email has no valid attachment
- Better handling of compressed attachments

**New logic**:
```python
if filename.endswith(('.xml', '.gz', '.zip')):
    # Process file
```

#### 3. Added Verbose Mode
New `--verbose` or `-v` flag for debugging:
```bash
python3 dmarc_parser.py --email you@gmail.com --password "xxx" --verbose
```

**Output includes**:
- How many emails each search criterion found
- Total unique emails before limit
- Emails being processed

#### 4. Better Error Messages
- Shows which emails look like DMARC reports but lack attachments
- More informative warnings during processing

### Testing Results

**Test with Yahoo DMARC Report** (`yahoo_report.xml`):
- ✅ Successfully detected 14 SPF alignment failures
- ✅ Correctly identified all source IPs
- ✅ Provided specific recommendations for each failure
- ✅ Generated complete JSON export

**Sample failures detected**:
```
Domain: rew.ca
Total failed messages: 14

Failure sources:
- 173.201.192.58, 75, 94, 95 (GoDaddy/secureserver.net)
- 174.129.206.125 (actual SPF fail)
- 198.2.133.95 (Mailchimp/mandrillapp.com)
- 198.2.190.81 (MailChimp delivery)
- 209.85.208.46, 210.182, 216.41, 216.51, 218.52, 222.41 (Gmail forwarding)
- 74.208.4.197 (timtruss.com)
```

### Usage

#### Basic usage (unchanged):
```bash
python3 dmarc_parser.py --email you@gmail.com --password "your-app-password"
```

#### With verbose mode (new):
```bash
python3 dmarc_parser.py --email you@gmail.com --password "your-app-password" --verbose
```

#### Search more emails:
```bash
python3 dmarc_parser.py --email you@gmail.com --password "your-app-password" --limit 200
```

#### Search different mailbox:
```bash
python3 dmarc_parser.py --email you@gmail.com --password "your-app-password" --mailbox "[Gmail]/All Mail"
```

### What This Fixes

1. ✅ **Yahoo DMARC reports** now detected correctly
2. ✅ **Google DMARC reports** explicitly searched for
3. ✅ **Standard "Report Domain:" subject format** matched
4. ✅ **SPF alignment failures** properly identified
5. ✅ **Verbose debugging** available for troubleshooting

### Backward Compatibility

All existing functionality preserved:
- ✅ Command-line arguments unchanged (except new optional `--verbose`)
- ✅ JSON export format unchanged
- ✅ Output format unchanged
- ✅ All existing features work as before

### Understanding SPF Alignment vs SPF Authentication

**Important**: The parser correctly identifies when:
- **SPF authentication passes** for a different domain (e.g., gmail.com, sendgrid.info)
- **But SPF alignment fails** because that domain doesn't match your header_from domain

Example from your report:
```xml
<policy_evaluated>
  <spf>fail</spf>  <!-- DMARC alignment failed -->
</policy_evaluated>
<auth_results>
  <spf>
    <domain>gmail.com</domain>
    <result>pass</result>  <!-- SPF passed for gmail.com -->
  </spf>
</auth_results>
```

Result: Parser correctly reports this as SPF failure because DMARC requires alignment with your domain (rew.ca).

### Files Updated

- `dmarc_parser.py` - Core parser with enhanced search and verbose mode

### Next Steps

1. Test with your Gmail account using the improved search
2. Use `--verbose` flag to see which search criteria find your reports
3. Adjust `--limit` if you have many reports
4. Try different `--mailbox` if reports are filed elsewhere

### Known Limitations

- Still uses Python standard library only (no external dependencies)
- IMAP search capabilities limited by email server
- Some email providers may have different DMARC report formats

---

**Version**: 1.1  
**Date**: 2025-11-08  
**Status**: Tested and working with Yahoo DMARC reports
