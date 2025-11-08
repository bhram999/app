# 📦 Download & Installation Instructions

## What You're Getting

A complete, production-ready Python DMARC parser that:
- ✅ Fetches reports automatically from Gmail
- ✅ Identifies DKIM, SPF, and alignment failures
- ✅ Provides actionable recommendations
- ✅ Works standalone (no dependencies!)
- ✅ Jenkins-ready with sample configurations

---

## 📥 Files to Download

Download these files to your local machine or Jenkins server:

### Core Files (Required)
1. **`dmarc_parser.py`** - Main parser script
2. **`DMARC_README.md`** - Complete documentation
3. **`QUICKSTART.md`** - Quick start guide

### Optional Files
4. **`run_dmarc_parser.sh`** - Wrapper script with env variables
5. **`.env.dmarc.example`** - Configuration template
6. **`jenkins_dmarc_job.sh`** - Jenkins shell script
7. **`Jenkinsfile`** - Jenkins pipeline definition
8. **`test_dmarc_parser.py`** - Test with local XML files
9. **`sample_dmarc_report.xml`** - Sample report for testing

---

## 🚀 Installation Steps

### Local Machine Installation

1. **Download the files**
   ```bash
   # Download all files to a directory
   mkdir ~/dmarc-parser
   cd ~/dmarc-parser
   
   # Copy the files here
   ```

2. **Make scripts executable**
   ```bash
   chmod +x dmarc_parser.py
   chmod +x run_dmarc_parser.sh
   chmod +x test_dmarc_parser.py
   ```

3. **Test the installation**
   ```bash
   python3 --version  # Should be 3.7 or higher
   python3 dmarc_parser.py --help
   ```

4. **Run a test with sample data**
   ```bash
   python3 test_dmarc_parser.py sample_dmarc_report.xml
   ```

5. **Configure your credentials**
   ```bash
   cp .env.dmarc.example .env.dmarc
   nano .env.dmarc  # Edit with your Gmail credentials
   ```

6. **Run the parser**
   ```bash
   ./run_dmarc_parser.sh
   # OR
   python3 dmarc_parser.py --email you@gmail.com --password "your-app-password"
   ```

---

### Jenkins Installation

1. **Upload files to Jenkins server**
   ```bash
   # SSH to Jenkins server
   ssh jenkins-server
   
   # Create directory
   sudo mkdir -p /var/jenkins_home/scripts/dmarc
   cd /var/jenkins_home/scripts/dmarc
   
   # Upload files here (use scp, git, or web interface)
   ```

2. **Set permissions**
   ```bash
   sudo chmod +x dmarc_parser.py jenkins_dmarc_job.sh
   sudo chown -R jenkins:jenkins /var/jenkins_home/scripts/dmarc
   ```

3. **Create Jenkins credentials**
   - Go to Jenkins → Manage Jenkins → Manage Credentials
   - Add → Secret text
   - ID: `gmail-dmarc-credentials`
   - Add your Gmail email and App Password

4. **Create Jenkins job**
   
   **Option A: Freestyle Project**
   - New Item → Freestyle project
   - Build Triggers → Build periodically: `H 2 * * *`
   - Build → Execute shell:
   ```bash
   cd /var/jenkins_home/scripts/dmarc
   bash jenkins_dmarc_job.sh
   ```

   **Option B: Pipeline Project**
   - New Item → Pipeline
   - Pipeline → Definition: Pipeline script from SCM (if using git)
   - Or paste the Jenkinsfile content directly

5. **Run and test**
   - Click "Build Now"
   - Check Console Output
   - Review generated reports in workspace

---

## 🔐 Setting Up Gmail Access

### Step 1: Enable IMAP

1. Open Gmail
2. Click Settings (gear icon) → See all settings
3. Go to "Forwarding and POP/IMAP" tab
4. Enable IMAP
5. Save Changes

### Step 2: Enable 2-Step Verification

1. Go to: https://myaccount.google.com/security
2. Find "2-Step Verification"
3. Click "Get started" and follow instructions
4. Complete setup

### Step 3: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select app: "Mail" (or "Other" → "DMARC Parser")
3. Select device: "Other" → "DMARC Parser"
4. Click "Generate"
5. Copy the 16-character password (format: xxxx-xxxx-xxxx-xxxx)
6. Remove spaces when using: xxxxxxxxxxxxxxxx

**⚠️ Important**: 
- Save this password securely
- Never commit it to version control
- You can't view it again (but can generate a new one)
- Use THIS password, not your regular Gmail password

---

## ✅ Verification

### Test 1: Local XML File
```bash
python3 test_dmarc_parser.py sample_dmarc_report.xml
```
**Expected**: Colorful output showing 2 failures

### Test 2: Gmail Connection
```bash
python3 dmarc_parser.py \
  --email your@gmail.com \
  --password "your-app-password" \
  --limit 5
```
**Expected**: Connects to Gmail and processes reports

### Test 3: Full Run with Export
```bash
python3 dmarc_parser.py \
  --email your@gmail.com \
  --password "your-app-password" \
  --limit 50 \
  --output test_report.json
```
**Expected**: JSON file created with results

---

## 📂 Recommended Directory Structure

```
/opt/dmarc-parser/                 # Or any directory you prefer
├── dmarc_parser.py                # Main script
├── run_dmarc_parser.sh           # Wrapper script
├── .env.dmarc                     # Your credentials (DO NOT COMMIT!)
├── .env.dmarc.example            # Template
├── test_dmarc_parser.py          # Test script
├── sample_dmarc_report.xml       # Sample data
├── jenkins_dmarc_job.sh          # Jenkins script
├── Jenkinsfile                    # Pipeline definition
├── DMARC_README.md               # Full documentation
├── QUICKSTART.md                  # Quick start guide
├── reports/                       # Directory for reports
│   ├── dmarc_failures_20250115.json
│   └── dmarc_failures_20250116.json
└── logs/                          # Optional: logs directory
    └── dmarc_parser.log
```

---

## 🔧 Configuration Options

### Environment Variables Method

Create `.env.dmarc`:
```bash
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx
IMAP_SERVER=imap.gmail.com
MAILBOX=INBOX
LIMIT=50
OUTPUT_FILE=dmarc_failures.json
```

Run with:
```bash
./run_dmarc_parser.sh
```

### Command Line Method

```bash
python3 dmarc_parser.py \
  --email your@gmail.com \
  --password "xxxxxxxxxxxxxxxx" \
  --server imap.gmail.com \
  --mailbox INBOX \
  --limit 50 \
  --output dmarc_failures.json
```

---

## 📅 Setting Up Automated Runs

### Cron (Linux/Mac)

Edit crontab:
```bash
crontab -e
```

Add line:
```bash
# Run daily at 2 AM
0 2 * * * cd /opt/dmarc-parser && ./run_dmarc_parser.sh >> logs/cron.log 2>&1
```

### Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 2:00 AM
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `C:\path\to\dmarc_parser.py --email you@gmail.com --password "xxx"`

### Jenkins (Production)

See "Jenkins Installation" section above

---

## 🐛 Common Issues & Solutions

### Issue: "ModuleNotFoundError"
**Solution**: The script uses only standard library - ensure Python 3.7+
```bash
python3 --version
```

### Issue: "Authentication failed"
**Solution**: Use App Password, not regular password
- Generate at: https://myaccount.google.com/apppasswords
- Enable 2-Step Verification first

### Issue: "No reports found"
**Solution**: 
- Check DMARC is configured for your domain
- Reports take 24-48 hours to arrive
- Try increasing `--limit`
- Check mailbox name (try `[Gmail]/All Mail`)

### Issue: "Permission denied" (Linux/Mac)
**Solution**: Make script executable
```bash
chmod +x dmarc_parser.py
```

### Issue: "Connection timeout"
**Solution**:
- Check firewall allows port 993
- Verify internet connection
- Try with `--server imap.gmail.com` explicitly

---

## 📊 Understanding Output

### Terminal Output Colors

- 🔴 **Red**: Failures and critical issues
- 🟢 **Green**: Success and passing checks
- 🟡 **Yellow**: Warnings and notices
- 🔵 **Blue**: Information
- 🟣 **Purple**: Recommendations

### JSON Output Structure

```json
{
  "generated_at": "2025-01-15T10:30:00",
  "total_reports": 15,
  "total_failures": 3,
  "failures": [
    {
      "domain": "example.com",
      "source_ip": "192.0.2.1",
      "count": 25,
      "dkim_result": "fail",
      "spf_result": "pass",
      "disposition": "none",
      ...
    }
  ],
  "all_reports": [...]
}
```

---

## 🔒 Security Best Practices

1. **Credentials Storage**
   - Never commit `.env.dmarc` to git
   - Use `chmod 600 .env.dmarc` to restrict access
   - Use Jenkins credentials for production

2. **App Password Management**
   - Generate separate passwords for different environments
   - Rotate passwords every 90 days
   - Revoke unused passwords

3. **Report Storage**
   - Store reports in secure location
   - Set up automatic cleanup (delete after 30 days)
   - Consider encryption for sensitive data

4. **Access Control**
   - Limit who can run the script
   - Use service accounts in production
   - Audit access logs regularly

---

## 📚 Next Steps

1. ✅ Download all files
2. ✅ Set up Gmail App Password
3. ✅ Test with sample XML file
4. ✅ Test with real Gmail connection
5. ✅ Review first report
6. ✅ Set up automated runs (cron/Jenkins)
7. ✅ Configure email alerts for failures
8. ✅ Document your DMARC infrastructure

---

## 🆘 Getting Help

- **Full Documentation**: See `DMARC_README.md`
- **Quick Start**: See `QUICKSTART.md`
- **Test Script**: Run `test_dmarc_parser.py` with sample data
- **Help Command**: `python3 dmarc_parser.py --help`

---

## 📝 Quick Reference

```bash
# Test with sample data
python3 test_dmarc_parser.py sample_dmarc_report.xml

# Quick check (last 20 reports)
python3 dmarc_parser.py --email you@gmail.com --password "xxx" --limit 20

# Full analysis
python3 dmarc_parser.py --email you@gmail.com --password "xxx" --limit 100

# With env file
./run_dmarc_parser.sh

# Custom output
python3 dmarc_parser.py --email you@gmail.com --password "xxx" --output custom.json
```

---

**🎉 You're all set! Start analyzing your DMARC reports now.**
