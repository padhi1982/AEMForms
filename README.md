# 🤖 AEM Forms Agent Workflow

An intelligent PDF-to-AEM form converter using AI agents and OpenAI LLM.

## 📋 Features

- **Agent 1 - Parser**: Extracts form structure from PDF using GPT-4o
- **Agent 2 - Builder**: Generates responsive HTML forms from extracted structure
- **Agent 3 - Mapper**: Maps forms to AEM component specifications
- **Web GUI**: User-friendly interface for uploading PDFs and viewing outputs
- **Local Execution**: Runs entirely on your machine

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (free trial available)

### Step 1: Get OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign up or log in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Step 2: Setup & Configure

```bash
# Run the setup script
./setup.sh
```

This will:
- Install all dependencies
- Prompt you for your OpenAI API key
- Validate the key works
- Save it securely to `~/.aem_forms_config.json`

### Step 3: Start the Application

```bash
python3 app.py
```

### Step 4: Open in Browser

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

### Setting API Key Manually

**Option 1: Environment Variable**
```bash
export OPENAI_API_KEY='sk-...'
python3 app.py
```

**Option 2: Config File**
The setup script saves it to: `~/.aem_forms_config.json`

**Option 3: Interactive Setup**
```bash
python3 config.py
```

### Verify API Key

```bash
python3 -c "
from config import validate_openai_key
validate_openai_key()
"
```

## 🏗️ Project Structure

```
PDF-AEMforms/
├── app.py                 # Flask web server
├── agent_parser.py        # PDF → JSON (LLM-powered)
├── agent_builder.py       # JSON → HTML form
├── agent_mapper.py        # HTML → AEM specs
├── config.py              # Configuration management
├── setup.sh               # Setup script
├── templates/
│   └── index.html         # Web UI template
├── uploads/               # Uploaded PDFs
└── outputs/               # Generated files
```

## 🤖 How It Works

### Agent 1: Parser (PDF Analysis)
- Reads PDF text with `pdfplumber`
- Sends to OpenAI GPT-4o for intelligent form extraction
- Outputs structured JSON with fields, types, and validation rules

### Agent 2: Builder (HTML Generation)
- Takes JSON from Parser
- Uses Jinja2 templates to generate responsive HTML
- Includes dynamic field visibility rules

### Agent 3: Mapper (AEM Integration)
- Parses HTML with BeautifulSoup
- Maps HTML form fields to AEM components
- Generates deployment specification

## 📊 Supported Field Types

- Text input
- Email
- Phone number
- Numeric
- Date
- Checkbox
- Radio buttons
- Dropdown/Select
- Text area
- File upload

## 🔧 Troubleshooting

### OpenAI API Key Issues
```bash
# Re-run setup
python3 config.py

# Or check current setup
python3 -c "from config import get_config; print(get_config())"
```

### Port Already in Use
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9
```

### PDF Extraction Issues
- Ensure PDF is not password protected
- Try converting scanned PDFs to text-based PDFs first
- Check PDF size (max 50MB)

## 📚 Dependencies

- Flask - Web framework
- pdfplumber - PDF text extraction
- BeautifulSoup4 - HTML parsing
- Jinja2 - Template engine
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
