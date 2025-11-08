# DMARC Report Parser

A standalone Python script to fetch and analyze DMARC aggregate reports from Gmail, identifying DKIM, SPF, and DMARC alignment failures with detailed recommendations.

## Features

- 📧 **Automatic Email Fetching**: Connects to Gmail via IMAP to retrieve DMARC reports
- 🔍 **Comprehensive Parsing**: Handles XML, gzipped, and zipped DMARC aggregate reports
- ⚠️ **Failure Detection**: Identifies DKIM, SPF, and alignment failures
- 📊 **Detailed Analysis**: Shows source IPs, failure counts, and authentication details
- 💡 **Smart Recommendations**: Provides actionable steps to resolve issues
- 🎨 **Colored Output**: Easy-to-read terminal output with color coding
- 💾 **JSON Export**: Exports full reports for further analysis or integration

## Requirements

- Python 3.7 or higher
- Gmail account with App Password (for IMAP access)
- No external dependencies - uses only Python standard library

## Setup

### 1. Enable Gmail IMAP Access

1. Go to Gmail Settings → See all settings → Forwarding and POP/IMAP
2. Enable IMAP
3. Save changes

### 2. Generate Gmail App Password

**Important**: You cannot use your regular Gmail password. You must create an App Password.

1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to Security → 2-Step Verification (enable if not already)
3. Go to App Passwords: https://myaccount.google.com/apppasswords
4. Select app: "Mail" or "Other (Custom name)"
5. Generate password
6. Copy the 16-character password (remove spaces)

### 3. Download the Script

Copy `dmarc_parser.py` to your local machine or Jenkins server.

## Usage

### Basic Usage

```bash
python3 dmarc_parser.py --email your-email@gmail.com --password "your-app-password"
```

### Advanced Options

```bash
# Process more emails
python3 dmarc_parser.py --email your-email@gmail.com --password "your-app-password" --limit 100

# Specify output file
python3 dmarc_parser.py --email your-email@gmail.com --password "your-app-password" --output my_report.json

# Search different mailbox
python3 dmarc_parser.py --email your-email@gmail.com --password "your-app-password" --mailbox "[Gmail]/All Mail"

# Use different IMAP server
python3 dmarc_parser.py --email your-email@gmail.com --password "your-app-password" --server imap.gmail.com
```

### Command Line Options

- `--email`: Your Gmail email address (required)
- `--password`: Gmail App Password (required)
- `--mailbox`: Mailbox to search (default: INBOX)
- `--limit`: Maximum emails to process (default: 50)
- `--output`: JSON output file path (default: dmarc_failures.json)
- `--server`: IMAP server (default: imap.gmail.com)

## Output

The script provides two types of output:

### 1. Terminal Output (Colored)

Real-time colored output showing:
- Connection status
- Reports found and processed
- Detailed failure information:
  - Source IP addresses
  - Message counts
  - DKIM/SPF results
  - Disposition (none/quarantine/reject)
  - Domain information
- Specific recommendations for each failure
- Summary statistics

### 2. JSON Export

Complete report saved to `dmarc_failures.json` (or custom path) containing:
```json
{
  "generated_at": "2025-01-15T10:30:00",
  "total_reports": 15,
  "total_failures": 3,
  "failures": [...],
  "all_reports": [...]
}
```

## Understanding the Output

### Failure Information

Each failure shows:
- **Source IP**: IP address that sent the email
- **Count**: Number of messages from this source
- **Header From**: Domain in the From header
- **Date**: When the report was generated
- **Reporter**: Organization that sent the DMARC report
- **DKIM Result**: pass/fail status with details
- **SPF Result**: pass/fail status with details
- **Disposition**: How the email was handled (none/quarantine/reject)

### Recommendations

The script provides specific recommendations based on failure type:

**DKIM Failures**:
- Verify DKIM signing is enabled
- Check private key configuration
- Ensure DNS records are correct
- Verify selector and domain match

**SPF Failures**:
- Add authorized IPs to SPF record
- Review SPF record syntax
- Check DNS lookup limit
- Verify all mail servers are included

**Disposition Issues**:
- REJECT: Immediate action required
- QUARANTINE: Messages going to spam
- NONE: Monitoring mode

## Running on Jenkins

### 1. Create Jenkins Job

1. New Item → Freestyle project
2. Configure Source Code Management (if storing in repo)
3. Build Triggers → Build periodically
   - Schedule: `H 2 * * *` (daily at 2 AM)
   - Or: `H */6 * * *` (every 6 hours)

### 2. Add Build Step

**Execute Shell**:
```bash
#!/bin/bash
cd /path/to/script
python3 dmarc_parser.py \
  --email "${GMAIL_EMAIL}" \
  --password "${GMAIL_APP_PASSWORD}" \
  --limit 100 \
  --output "reports/dmarc_failures_$(date +%Y%m%d_%H%M%S).json"
```

### 3. Configure Credentials

Store Gmail credentials securely:
1. Jenkins → Manage Jenkins → Manage Credentials
2. Add → Secret text for email and password
3. Reference in job: `${GMAIL_EMAIL}`, `${GMAIL_APP_PASSWORD}`

### 4. Add Post-Build Actions

Optional:
- Email notifications on failures
- Archive artifacts (JSON reports)
- Trigger other jobs based on findings

## Troubleshooting

### Common Issues

**"Authentication failed"**
- Use App Password, not regular password
- Ensure 2-Step Verification is enabled
- Check email address is correct

**"No DMARC reports found"**
- Check DMARC policy is published for your domain
- Verify you're receiving reports (check email)
- Try increasing `--limit` or checking different mailbox
- DMARC reports may take 24-48 hours to arrive

**"Connection timeout"**
- Check firewall settings
- Ensure IMAP port 993 is not blocked
- Verify internet connectivity

**"Permission denied" on Jenkins**
- Ensure Python 3 is installed: `python3 --version`
- Make script executable: `chmod +x dmarc_parser.py`
- Check file paths in Jenkins job

## Security Best Practices

1. **Never commit passwords**: Use environment variables or Jenkins credentials
2. **Restrict file permissions**: `chmod 600` for credential files
3. **Use App Passwords**: Never use your main Gmail password
4. **Rotate credentials**: Change App Passwords periodically
5. **Audit access**: Review who has access to credentials

## Sample Output

```
╔═══════════════════════════════════════════════════════════╗
║           DMARC REPORT PARSER & ANALYZER                 ║
║        Email Authentication Failure Detection            ║
╚═══════════════════════════════════════════════════════════╝

Connecting to imap.gmail.com...
✓ Connected successfully

Found 15 potential DMARC report emails

⚠ FAILURES FOUND in report from google.com for domain yourdomain.com
✓ All passed in report from yahoo.com for yourdomain.com

================================================================================
DMARC AUTHENTICATION FAILURES REPORT
================================================================================

Domain: yourdomain.com
────────────────────────────────────────────────────────────────────────────────
Total failed messages: 45

Failure #1:
  Source IP: 192.168.1.100
  Count: 45 messages
  Header From: yourdomain.com
  Date: 2025-01-15
  Reporter: google.com
  ✗ DKIM: FAIL
    - Domain: yourdomain.com, Result: fail
  ✓ SPF: PASS
  Disposition: none

  Recommendations:
    DKIM Failure:
      • Verify DKIM signing is enabled on your mail server
      • Check DKIM private key configuration
      • Ensure DKIM DNS record is published correctly
      • Verify selector and domain match in email headers
    General recommendations:
      • Check IP reputation for 192.168.1.100
      • Verify this IP is authorized to send on your behalf
      • Use DMARC alignment to ensure domain consistency

SUMMARY:
Total reports analyzed: 15
Reports with failures: 1
Total failure records: 1
Total failed messages: 45

✓ Full report exported to: dmarc_failures.json

Done!
```

## Advanced Usage

### Filtering Reports by Date

Modify the script to add date filtering:
```python
# In fetch_dmarc_reports method, add:
search_criteria = '(SINCE "01-Jan-2025")'
```

### Integrating with Other Tools

Use the JSON export with other tools:
```bash
# Process with jq
cat dmarc_failures.json | jq '.failures[] | select(.count > 10)'

# Import into database
python3 import_to_db.py --input dmarc_failures.json
```

### Email Notifications

Add email alerts:
```bash
# After running script
if [ -s dmarc_failures.json ]; then
  mail -s "DMARC Failures Detected" admin@yourdomain.com < dmarc_failures.json
fi
```

## License

This script is provided as-is for analyzing DMARC reports.

## Support

For issues or questions:
1. Check troubleshooting section
2. Verify Gmail settings and credentials
3. Test with `--limit 10` for faster debugging

## DMARC Resources

- [DMARC.org](https://dmarc.org/) - Official DMARC specification
- [Google DMARC Documentation](https://support.google.com/a/answer/2466580)
- [DMARC Record Check](https://mxtoolbox.com/dmarc.aspx)
- [SPF Record Check](https://mxtoolbox.com/spf.aspx)
- [DKIM Record Check](https://mxtoolbox.com/dkim.aspx)
