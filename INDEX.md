# 📋 DMARC Parser - File Index

## 🎯 Start Here

New to DMARC parsing? Start with these files in order:

1. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 3 steps
2. **[DOWNLOAD_INSTRUCTIONS.md](DOWNLOAD_INSTRUCTIONS.md)** - Installation guide
3. **[DMARC_README.md](DMARC_README.md)** - Complete documentation

---

## 📦 All Files Overview

### 🔴 Core Files (Must Have)

| File | Size | Purpose |
|------|------|---------|
| `dmarc_parser.py` | 18KB | **Main parser script** - This is what you run |
| `DMARC_README.md` | 9.4KB | Complete documentation with examples |
| `QUICKSTART.md` | 5.2KB | Quick start guide - fastest way to get started |

**Download these three files minimum to use the parser.**

---

### 🟡 Configuration Files (Recommended)

| File | Size | Purpose |
|------|------|---------|
| `.env.dmarc.example` | 509B | Template for storing credentials securely |
| `run_dmarc_parser.sh` | 1.6KB | Wrapper script that loads credentials from .env file |

**Download these to simplify credential management.**

---

### 🟢 Jenkins Integration (For Production)

| File | Size | Purpose |
|------|------|---------|
| `Jenkinsfile` | 3.8KB | Jenkins Pipeline definition (declarative) |
| `jenkins_dmarc_job.sh` | 2.3KB | Shell script for Jenkins freestyle jobs |
| `DOWNLOAD_INSTRUCTIONS.md` | 9.6KB | Detailed Jenkins setup instructions |

**Download these if you want to run on Jenkins for scheduled execution.**

---

### 🔵 Testing & Examples

| File | Size | Purpose |
|------|------|---------|
| `test_dmarc_parser.py` | 1.3KB | Test the parser without Gmail connection |
| `sample_dmarc_report.xml` | 2.3KB | Sample DMARC report for testing |
| `dmarc_requirements.txt` | 121B | Python dependencies (none - uses stdlib!) |

**Download these to test before connecting to Gmail.**

---

## 🚀 Quick Start Paths

### Path 1: Just Want to Run It Now
```
1. Download: dmarc_parser.py
2. Get Gmail App Password
3. Run: python3 dmarc_parser.py --email you@gmail.com --password "xxx"
```

### Path 2: Proper Local Setup
```
1. Download: dmarc_parser.py, .env.dmarc.example, run_dmarc_parser.sh
2. Configure: cp .env.dmarc.example .env.dmarc (edit with your credentials)
3. Run: ./run_dmarc_parser.sh
```

### Path 3: Production Jenkins Setup
```
1. Download: All files
2. Read: DOWNLOAD_INSTRUCTIONS.md
3. Follow: Jenkins Installation section
4. Schedule: Daily automated runs
```

### Path 4: Test First (No Gmail Needed)
```
1. Download: dmarc_parser.py, test_dmarc_parser.py, sample_dmarc_report.xml
2. Run: python3 test_dmarc_parser.py sample_dmarc_report.xml
3. Review: Output shows how parser works
```

---

## 📖 Documentation Hierarchy

```
INDEX.md (You are here)
    ├── QUICKSTART.md ..................... 5-minute quick start
    │   └── 3 simple commands to run the parser
    │
    ├── DOWNLOAD_INSTRUCTIONS.md .......... Installation guide
    │   ├── Local machine setup
    │   ├── Jenkins setup
    │   ├── Gmail App Password guide
    │   └── Troubleshooting
    │
    └── DMARC_README.md .................... Complete documentation
        ├── Features overview
        ├── All command-line options
        ├── Output interpretation
        ├── Jenkins integration details
        ├── Advanced usage
        └── DMARC resources
```

---

## 🎯 Use Case → Files Needed

### Use Case 1: Quick One-Time Analysis
**Files**: `dmarc_parser.py`
```bash
python3 dmarc_parser.py --email you@gmail.com --password "xxx"
```

### Use Case 2: Regular Manual Runs
**Files**: `dmarc_parser.py`, `.env.dmarc.example`, `run_dmarc_parser.sh`
```bash
cp .env.dmarc.example .env.dmarc
nano .env.dmarc
./run_dmarc_parser.sh
```

### Use Case 3: Automated Daily Reports
**Files**: All Jenkins files + core files
- Set up Jenkins job with `Jenkinsfile`
- Schedule with cron expression: `H 2 * * *`

### Use Case 4: Test Without Email Access
**Files**: `dmarc_parser.py`, `test_dmarc_parser.py`, `sample_dmarc_report.xml`
```bash
python3 test_dmarc_parser.py sample_dmarc_report.xml
```

### Use Case 5: Integration with Other Tools
**Files**: `dmarc_parser.py` (run with `--output` flag)
```bash
python3 dmarc_parser.py --email you@gmail.com --password "xxx" --output report.json
# Then process report.json with other tools
```

---

## 🔑 Key Features

### What the Parser Does

✅ **Automatic Fetching**: Connects to Gmail via IMAP  
✅ **Comprehensive Parsing**: Handles XML, .gz, .zip formats  
✅ **Failure Detection**: Identifies DKIM, SPF, alignment issues  
✅ **Detailed Analysis**: Shows IPs, counts, authentication details  
✅ **Smart Recommendations**: Actionable steps for each failure  
✅ **Beautiful Output**: Color-coded terminal display  
✅ **JSON Export**: Machine-readable format for integration  
✅ **Zero Dependencies**: Uses only Python standard library  

---

## 📊 What You Get

### Terminal Output Example
```
DMARC AUTHENTICATION FAILURES REPORT
================================================================================

Domain: yourdomain.com
Total failed messages: 45

Failure #1:
  Source IP: 192.168.1.100
  Count: 45 messages
  ✗ DKIM: FAIL
  ✓ SPF: PASS
  
  Recommendations:
    • Verify DKIM signing is enabled
    • Check DKIM private key configuration
    • Ensure DKIM DNS record is published correctly
    ...
```

### JSON Export Structure
```json
{
  "generated_at": "2025-01-15T10:30:00",
  "total_reports": 15,
  "total_failures": 3,
  "failures": [ /* detailed failure objects */ ],
  "all_reports": [ /* all parsed reports */ ]
}
```

---

## 🛠️ Requirements

- **Python**: 3.7 or higher
- **Gmail**: Account with App Password (not regular password)
- **IMAP**: Enabled in Gmail settings
- **Dependencies**: None (uses standard library only!)

---

## 🔐 Security Notes

⚠️ **Important Security Practices**:

1. **Never commit credentials** to version control
2. **Use App Passwords** (16-char), not your regular Gmail password
3. **Set file permissions**: `chmod 600 .env.dmarc`
4. **Use Jenkins credentials** in production environments
5. **Rotate passwords** regularly (every 90 days)

---

## 💡 Tips

### First Time Users
- Start with `QUICKSTART.md`
- Test with `sample_dmarc_report.xml` first
- Use `--limit 10` for faster initial runs
- Read recommendations carefully

### Jenkins Users
- Read `DOWNLOAD_INSTRUCTIONS.md` Jenkins section
- Use Jenkins credentials store (never hardcode passwords)
- Set up email notifications for failures
- Archive reports as artifacts

### Power Users
- Parse JSON with `jq` for custom filtering
- Integrate with monitoring systems (Grafana, etc.)
- Set up database imports for historical tracking
- Create custom alerts based on thresholds

---

## 🆘 Help & Troubleshooting

### Quick Checks

✅ Python 3.7+ installed? `python3 --version`  
✅ Using App Password? (not regular password)  
✅ IMAP enabled in Gmail settings?  
✅ 2-Step Verification enabled?  
✅ Firewall allows port 993?  

### Get Help

- **Error: "Authentication failed"** → Check App Password setup
- **Error: "No reports found"** → Increase `--limit`, check DMARC policy
- **Error: "Connection timeout"** → Check firewall, network
- **Need examples** → See `DMARC_README.md` or `QUICKSTART.md`

---

## 📁 Recommended Download Sets

### Minimal Set (5 files)
```
✓ dmarc_parser.py
✓ QUICKSTART.md
✓ .env.dmarc.example
✓ test_dmarc_parser.py
✓ sample_dmarc_report.xml
```

### Complete Set (11 files)
```
✓ All files listed above
```

### Production Set (Jenkins)
```
✓ All files + read DOWNLOAD_INSTRUCTIONS.md carefully
```

---

## 🎓 Learning Resources

### Included in Package
- `QUICKSTART.md` - 5-minute tutorial
- `DMARC_README.md` - Complete guide with examples
- `DOWNLOAD_INSTRUCTIONS.md` - Setup instructions
- Sample XML file - See real DMARC report structure

### External Resources
- [DMARC.org](https://dmarc.org/) - Official specification
- [Google DMARC Docs](https://support.google.com/a/answer/2466580)
- [MXToolbox](https://mxtoolbox.com/dmarc.aspx) - Check your records

---

## ✅ Verification Checklist

Before running in production:

- [ ] Downloaded required files
- [ ] Python 3.7+ installed and verified
- [ ] Gmail App Password generated
- [ ] IMAP enabled in Gmail
- [ ] Tested with sample XML file
- [ ] Tested with Gmail connection (limit 5)
- [ ] Reviewed sample output
- [ ] Understood the recommendations
- [ ] Set up credential storage (.env or Jenkins)
- [ ] Configured automated runs (if needed)

---

## 🚀 Next Steps

1. **Choose your path** (Quick run / Local setup / Jenkins production)
2. **Download files** based on your path
3. **Follow guide** (QUICKSTART.md or DOWNLOAD_INSTRUCTIONS.md)
4. **Test** with sample data first
5. **Run** with real Gmail connection
6. **Review** failures and recommendations
7. **Fix** DMARC issues in your infrastructure
8. **Automate** for ongoing monitoring

---

**Ready to start?** → Open `QUICKSTART.md` for the fastest path to running the parser.

**Need detailed setup?** → Open `DOWNLOAD_INSTRUCTIONS.md` for complete installation guide.

**Want to understand everything?** → Open `DMARC_README.md` for comprehensive documentation.

---

*Last updated: 2025-01-15*
