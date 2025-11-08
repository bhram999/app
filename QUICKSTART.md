# DMARC Parser - Quick Start Guide

## 🚀 Quick Start (3 steps)

### Option 1: Run Directly with Command Line

```bash
python3 dmarc_parser.py \
  --email your-email@gmail.com \
  --password "your-app-password" \
  --limit 50
```

### Option 2: Run with Environment File

1. **Create configuration file**:
```bash
cp .env.dmarc.example .env.dmarc
nano .env.dmarc  # Edit with your credentials
```

2. **Run the wrapper script**:
```bash
./run_dmarc_parser.sh
```

### Option 3: Setup Jenkins Job

See detailed instructions in `DMARC_README.md` under "Running on Jenkins"

---

## 📋 Prerequisites Checklist

Before running, ensure you have:

- [ ] **Python 3.7+** installed (`python3 --version`)
- [ ] **Gmail App Password** generated (not your regular password!)
  - Go to: https://myaccount.google.com/apppasswords
  - Generate 16-character password
- [ ] **IMAP enabled** in Gmail settings
  - Gmail → Settings → Forwarding and POP/IMAP → Enable IMAP

---

## 🔑 Getting Gmail App Password

**IMPORTANT**: You CANNOT use your regular Gmail password. Follow these steps:

1. **Enable 2-Step Verification** (if not already enabled)
   - Visit: https://myaccount.google.com/security
   - Turn on 2-Step Verification

2. **Generate App Password**
   - Visit: https://myaccount.google.com/apppasswords
   - Select app: "Mail" or "Other (Custom name)"
   - Click "Generate"
   - Copy the 16-character password (without spaces)
   - Use this password in the `--password` parameter

---

## 📊 What You'll Get

### Terminal Output
- ✅ Real-time colored output
- 🔍 Detailed failure analysis
- 💡 Specific recommendations for each issue
- 📈 Summary statistics

### JSON Report File
- Complete machine-readable report
- All DMARC reports analyzed
- Detailed failure information
- Timestamps and metadata

---

## 🎯 Common Use Cases

### Case 1: Quick Check (Last 20 Reports)
```bash
python3 dmarc_parser.py \
  --email you@gmail.com \
  --password "xxxx-xxxx-xxxx-xxxx" \
  --limit 20
```

### Case 2: Comprehensive Analysis
```bash
python3 dmarc_parser.py \
  --email you@gmail.com \
  --password "xxxx-xxxx-xxxx-xxxx" \
  --limit 200 \
  --output reports/full_analysis_$(date +%Y%m%d).json
```

### Case 3: Search Specific Mailbox
```bash
python3 dmarc_parser.py \
  --email you@gmail.com \
  --password "xxxx-xxxx-xxxx-xxxx" \
  --mailbox "[Gmail]/All Mail"
```

---

## 🐛 Troubleshooting

### "Authentication failed"
- ✅ Use App Password (16 chars), NOT regular password
- ✅ Enable 2-Step Verification first
- ✅ Double-check email address

### "No reports found"
- ✅ DMARC policy must be published for your domain
- ✅ Reports take 24-48 hours to arrive
- ✅ Try `--limit 100` to search more emails
- ✅ Check if reports are in a different folder

### "Connection timeout"
- ✅ Check firewall allows port 993
- ✅ Verify internet connectivity
- ✅ Try `--server imap.gmail.com` explicitly

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `dmarc_parser.py` | Main script - run this |
| `run_dmarc_parser.sh` | Wrapper script with env vars |
| `.env.dmarc.example` | Template for credentials |
| `jenkins_dmarc_job.sh` | Jenkins shell script |
| `Jenkinsfile` | Jenkins pipeline definition |
| `DMARC_README.md` | Complete documentation |

---

## 💻 Jenkins Setup (Summary)

1. **Create Jenkins Job**
   - New Item → Pipeline
   - Use `Jenkinsfile` from this repo

2. **Add Credentials**
   - Manage Jenkins → Credentials
   - Add Secret Text for email & password
   - ID: `gmail-dmarc-credentials`

3. **Configure Schedule**
   - Build Triggers → Build periodically
   - Schedule: `H 2 * * *` (daily at 2 AM)

4. **Save & Run**
   - Reports saved in workspace/reports/
   - Archived as Jenkins artifacts

---

## 🎓 Understanding DMARC Failures

### What the script checks:

1. **DKIM (DomainKeys Identified Mail)**
   - Verifies email signature
   - Failure = Email may be forged

2. **SPF (Sender Policy Framework)**
   - Checks if sending IP is authorized
   - Failure = Unauthorized server sent email

3. **DMARC Alignment**
   - Ensures domains match correctly
   - Failure = Domain mismatch

### Severity Levels:

- 🔴 **REJECT**: Emails are being blocked (CRITICAL)
- 🟡 **QUARANTINE**: Emails going to spam (WARNING)
- 🔵 **NONE**: Monitoring only (INFO)

---

## 📞 Next Steps

1. Run the script with your credentials
2. Review any failures found
3. Follow the recommendations provided
4. Fix issues in your email infrastructure
5. Re-run to verify fixes
6. Setup Jenkins for automated monitoring

---

## ⚠️ Security Notes

- Never commit `.env.dmarc` to git
- Use environment variables in production
- Rotate App Passwords regularly
- Restrict access to credential files
- Use `chmod 600 .env.dmarc` for security

---

## 📖 More Help

See `DMARC_README.md` for:
- Detailed command-line options
- Complete Jenkins setup guide
- Sample output explanations
- Advanced use cases
- Integration examples

---

**Ready to start?**

```bash
# 1. Generate App Password at: https://myaccount.google.com/apppasswords
# 2. Run the script:
python3 dmarc_parser.py --email your@gmail.com --password "your-app-password"
```

🎉 That's it! The script will analyze your DMARC reports and show you any authentication failures.
