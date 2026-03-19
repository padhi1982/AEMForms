# 🤖 AEM Forms Agent Workflow

An intelligent PDF-to-AEM form converter using AI agents and Google Gemini LLM.

> **Convert multi-page PDF forms into structured JSON schemas and interactive HTML forms with AI-powered field detection.**

## ✨ Features

- **🤖 AI-Powered Extraction**: Uses Google Gemini (free) or OpenAI GPT-4o to analyze forms
- **3-Agent Workflow**: 
  - **Agent 1 (Parser)**: Extracts form structure from PDF
  - **Agent 2 (Builder)**: Generates responsive HTML forms
  - **Agent 3 (Mapper)**: Maps to AEM component specifications
- **🎨 Web GUI**: User-friendly interface for PDF upload and real-time processing
- **💾 JSON Output**: Generates headless form schemas for integration
- **🚀 Local Execution**: Runs entirely on your machine
- **🆓 Free LLM Option**: Works with Google Gemini (no quota limits)
- **⚡ Fast Processing**: Pages 2-11 extraction optimized for large documents

## 📊 Test Results

Successfully tested with **Inherited IRA Application** PDF:
- **Total Fields Detected**: 246+ form fields
- **Pages Processed**: Pages 2-11 (18-page document)
- **Processing Time**: ~24 seconds with Gemini API
- **Sections Identified**: 10+ form sections with proper hierarchy
- **Field Types**: Text, Checkbox, Date, Select, Textarea

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API key (**FREE**) or OpenAI API key (optional)

### Option 1: Using Google Gemini (Recommended - FREE)

```bash
# Clone the repository
git clone https://github.com/padhi1982/AEMforms.git
cd AEMforms

# Install dependencies
pip install -r requirements.txt

# Setup Gemini API (interactive)
python3 setup_gemini_simple.py

# Start the application
export LLM_PROVIDER=gemini
python3 app.py
```

**To get a free Gemini API key:**
1. Go to https://aistudio.google.com/apikey
2. Click "Create API key"
3. Copy your API key
4. Paste it when prompted during setup

### Option 2: Using OpenAI (Optional Fallback)

```bash
python3 setup_gemini_simple.py
# When prompted, enter your OpenAI API key (starts with sk-)
```

### Step 3: Open in Browser

Navigate to: **http://localhost:5000**

## 📝 Usage

1. **Upload a PDF**: Click the upload area or drag-and-drop your form PDF
2. **Wait for Processing**:
   - Agent 1 (Parser): Analyzes PDF with LLM
   - Agent 2 (Builder): Creates HTML form
   - Agent 3 (Mapper): Generates AEM specs
3. **View Results**:
   - Headless JSON Form
   - HTML Form Preview
   - AEM Component Specifications

## 📁 Generated Files

Files are saved in `/outputs/<filename>/`:
- `headless_form.json` - Form structure
- `index.html` - Interactive HTML form
- `aem_spec_sheet.json` - AEM component mapping

## 🔑 API Key Management

### Setting Gemini API Key (Recommended)

**Option 1: Interactive Setup**
```bash
python3 setup_gemini_simple.py
```

**Option 2: Manual Configuration**
```bash
python3 config.py
```

**Option 3: Environment Variable**
```bash
export GEMINI_API_KEY='AIzaSy...'
python3 app.py
```

### Setting OpenAI API Key (Optional Fallback)

```bash
export OPENAI_API_KEY='sk-...'
python3 app.py
```

### API Key Storage

Keys are saved securely to: `~/.aem_forms_config.json`

### Verify API Key

```bash
python3 -c "
from config import validate_gemini_key, validate_openai_key
print('Gemini:', 'Valid' if validate_gemini_key() else 'Invalid')
print('OpenAI:', 'Valid' if validate_openai_key() else 'Invalid')
"
```

## 🏗️ Project Structure

```
PDF-AEMforms/
├── app.py                      # Flask web server (main entry point)
├── agent_parser.py             # Agent 1: PDF → JSON with LLM
├── agent_builder.py            # Agent 2: JSON → HTML form
├── agent_mapper.py             # Agent 3: HTML → AEM specs
├── config.py                   # API key & LLM configuration
├── index.html                  # GitHub Pages landing page
├── setup_gemini_simple.py      # Gemini API setup wizard
├── setup.sh                    # Installation script
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html              # Web UI template
├── aem-agent-workflow/         # Agent workflow implementation
├── uploads/                    # Uploaded PDF storage
├── outputs/                    # Generated form files
└── README.md                   # This file
```

## 🤖 How It Works

### Agent 1: Parser (PDF Analysis)
Extracts form structure from PDF documents using AI:
- Reads multi-page PDF with `pdfplumber`
- Focuses on pages 2-11 for form content
- Sends to Google Gemini LLM for intelligent analysis
- Detects form fields, types, labels, and validation rules
- Outputs structured JSON schema (246+ fields tested)

### Agent 2: Builder (HTML Generation)
Converts extracted JSON into interactive HTML:
- Uses Jinja2 templates for responsive design
- Implements field visibility rules
- Adds form validation and styling
- Creates standalone HTML form files

### Agent 3: Mapper (AEM Integration)
Maps form structure to Adobe Experience Manager:
- Parses HTML with BeautifulSoup
- Maps fields to AEM component types
- Generates deployment specifications
- Creates component configuration JSON

## 📊 Supported Field Types

- ✅ Text input
- ✅ Email
- ✅ Phone number
- ✅ Numeric
- ✅ Date
- ✅ Checkbox
- ✅ Radio buttons
- ✅ Dropdown/Select
- ✅ Text area
- ✅ File upload

## 🔧 Troubleshooting

### Gemini API Issues
```bash
# Re-run Gemini setup
python3 setup_gemini_simple.py

# Verify key works
python3 -c "from config import validate_gemini_key; print(validate_gemini_key())"
```

### Port Already in Use
```bash
# Kill existing Flask process
lsof -ti:5000 | xargs kill -9

# Or use different port
python3 app.py --port 5001
```

### PDF Extraction Issues
- ✓ Ensure PDF is not password protected
- ✓ Try converting scanned PDFs to text-based PDFs first
- ✓ Check PDF size (tested with 18-page documents)
- ✓ For complex layouts, pages 2-11 focus helps accuracy

### JSON Parsing Errors
The application includes robust JSON cleanup for LLM responses:
- Automatically handles escape sequence errors
- Falls back gracefully if parsing fails
- Retry with slightly different prompt if needed

## 📦 Dependencies

```
Flask==2.3.0
pdfplumber==0.11.0
reportlab==4.0.9
BeautifulSoup4==4.12.0
Jinja2==3.1.0
google-generativeai==0.3.0
openai==1.3.0
python-dotenv==1.0.0
requests==2.31.0
```

## 🆓 Free Tier Limits

**Google Gemini API (Free)**:
- 60 requests per minute
- No credit card required
- Unlimited free tier usage

**OpenAI API**:
- Free trial: $5 for 3 months
- Pay-as-you-go after trial

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Support

For issues and questions:
- Check the [README](README.md)
- Review [GitHub Issues](https://github.com/padhi1982/AEMforms/issues)
- Contact: padhi1982 on GitHub

## 📄 License

This project is open source and available under the MIT License.

---

**Made with ❤️ by padhi1982**
- reportlab - PDF generation
- openai - OpenAI API client

## 💳 OpenAI Pricing

- **GPT-4o**: $0.15 per 1M input tokens / $0.60 per 1M output tokens
- Typical form processing: ~$0.001-0.01 per PDF

[Check current pricing](https://openai.com/pricing)

## 🔒 Security Notes

- API keys are stored locally in `~/.aem_forms_config.json` with 600 permissions
- Never commit `.aem_forms_config.json` to version control
- PDFs are processed locally; only text is sent to OpenAI
- Session data stored in browser only

---

**Made with ❤️ for AEM Forms Development**
