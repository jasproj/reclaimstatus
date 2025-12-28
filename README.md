# Treasury Package Generator

A web-based automation system for generating Treasury Package documents. Clients fill out a single questionnaire, and the system populates all 21+ documents automatically, generating both a merged PDF and individual PDFs.

## 🎯 Features

- **Single Questionnaire**: Clients enter information once
- **Auto-Population**: All documents filled from one data source
- **Multiple Formats**: 
  - Single merged PDF (for Treasury mailing)
  - ZIP of individual PDFs (for records)
- **Secure Processing**: Data encrypted in transit, never stored permanently
- **Self-Service**: Clients can generate their own packages

## 📋 Documents Generated

1. Affidavit of Notary Presentment
2. Recording Cover Sheet
3. Pre-Offset Notice for Balanced Book Adjustment
4. Affidavit of Political Status
5. UCC-1 Finance Statement
6. UCC-1 Addendum
7. Power of Attorney
8. Private Security Agreement
9. Attachment A - Property List
10. Indemnity Bond/Lien
11. Hold Harmless & Indemnity Agreement
12. Copyright Affidavit
13. Common Law Copyright Notice
14. Legal Notice & Demand Definitions
15. Continuation of Additional Collateral
16. Act of Expatriation
17. Chargeback Order
18. International Registered Private Tracking
19. Appointment of Fiduciary
20. Private Banker's Acceptance
21. IRS Form 56 (Treasury Secretary)
22. IRS Form 1041-V
23. Actual and Constructive Notice
24. Non-Negotiable International Bill of Exchange

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Web Interface  │────▶│  Backend API     │────▶│  PDF Generator  │
│  (React/HTML)   │     │  (Node/Python)   │     │  (LibreOffice)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
   Questionnaire           Field Mapping            Merged PDF +
   Form Data               & Replacement            ZIP Package
```

## 🚀 Quick Start

### Option 1: Static HTML (No Backend)
Open `questionnaire.html` in a browser. Generates JSON data file for manual processing.

### Option 2: Full Stack (Recommended)
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/treasury-package-generator.git
cd treasury-package-generator

# Install dependencies
npm install
pip install -r requirements.txt

# Start development server
npm run dev
```

## 📁 Project Structure

```
treasury-package-generator/
├── README.md
├── package.json
├── requirements.txt
├── .env.example
├── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── questionnaire.html      # Standalone questionnaire
│   └── src/
│       └── TreasuryPackageForm.jsx
│
├── backend/
│   ├── server.js               # Express API server
│   ├── generator.py            # Document generation engine
│   └── routes/
│       └── generate.js
│
├── templates/                   # DOCX templates (not in repo)
│   └── .gitkeep
│
├── config/
│   └── field_mapping.json      # Field definitions
│
└── docs/
    └── SETUP.md
```

## ⚙️ Configuration

### Environment Variables (.env)
```env
PORT=3000
TEMPLATE_DIR=./templates
OUTPUT_DIR=./output
ENCRYPTION_KEY=your-32-char-encryption-key
```

### Field Mapping
Edit `config/field_mapping.json` to customize:
- Questionnaire fields
- Document-to-field mappings
- Derived field calculations

## 🔒 Security Considerations

### Sensitive Data Handling
- SSN and personal data encrypted with AES-256
- Data processed in memory, not persisted
- HTTPS required for production
- No data logging

### Recommendations
1. Use HTTPS (Let's Encrypt)
2. Implement rate limiting
3. Add CAPTCHA for public deployments
4. Consider session-based processing

## 📦 Deployment Options

### Vercel/Netlify (Frontend Only)
- Deploy `questionnaire.html` as static site
- Use serverless function for generation

### Docker
```bash
docker build -t treasury-generator .
docker run -p 3000:3000 treasury-generator
```

### VPS (Full Control)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm python3 python3-pip libreoffice

# Install and run
npm install
pip install -r requirements.txt
npm run start
```

## 🛠️ Development

### Running Tests
```bash
npm test
python -m pytest tests/
```

### Adding New Documents
1. Add DOCX template to `templates/`
2. Update `field_mapping.json` with field list
3. Test with sample data

## 📄 License

Private/Proprietary - Contact for licensing

## 🤝 Support

For issues or feature requests, contact [your email]

---

## Changelog

### v1.0.0 (2025-01-XX)
- Initial release
- 24 document templates
- Web questionnaire
- PDF merge & ZIP generation
