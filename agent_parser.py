import pdfplumber
import json
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re

# LLM Provider options
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'gemini')  # Default: gemini, fallback: openai

def get_llm_client():
    """Get LLM client based on provider"""
    provider = LLM_PROVIDER.lower()
    
    if provider == 'gemini':
        return get_gemini_client()
    elif provider == 'openai':
        return get_openai_client()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

def get_gemini_client():
    """Get Google Gemini client"""
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            "❌ google-generativeai not installed!\n"
            "Install with: pip install google-generativeai"
        )
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError(
            "❌ GOOGLE_API_KEY not set!\n"
            "Get your FREE API key from: https://ai.google.dev/\n"
            "Set it with: export GOOGLE_API_KEY='your-api-key-here'"
        )
    
    genai.configure(api_key=api_key)
    return genai

def get_openai_client():
    """Get OpenAI client from environment variable"""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "❌ openai not installed!\n"
            "Install with: pip install openai"
        )
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError(
            "❌ OPENAI_API_KEY not set!\n"
            "Get your API key from: https://platform.openai.com/api-keys\n"
            "Set it with: export OPENAI_API_KEY='your-api-key-here'"
        )
    return OpenAI(api_key=api_key)

def query_llm(prompt):
    """Query LLM to parse form structure"""
    provider = LLM_PROVIDER.lower()
    
    try:
        if provider == 'gemini':
            return query_gemini(prompt)
        elif provider == 'openai':
            return query_openai(prompt)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    except Exception as e:
        print(f"❌ LLM Error ({provider}): {str(e)}")
        raise

def query_gemini(prompt):
    """Query Google Gemini for form structure"""
    client = get_gemini_client()
    
    try:
        # Try models in order of preference (newer/faster first)
        model_names = [
            'gemini-2.5-flash',      # Latest and fastest
            'gemini-2.0-flash',      # Good performance
            'gemini-pro-latest',     # Pro models
            'gemini-2.5-pro',        # Pro option
            'gemini-flash-latest',   # Generic latest
        ]
        
        model = None
        selected_model = None
        
        for model_name in model_names:
            try:
                model = client.GenerativeModel(model_name)
                selected_model = model_name
                print(f"   Using model: {model_name}")
                break
            except Exception as e:
                # Model not found, try next
                continue
        
        if not model or not selected_model:
            raise ValueError("No available Gemini models found. Please check your API key.")
        
        message = f"""You are an expert form architect. Extract form structure from documents and return ONLY valid JSON.

{prompt}

IMPORTANT: Return ONLY the JSON object, no markdown, no extra text."""
        
        response = model.generate_content(message)
        content = response.text
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json_match.group(0)
        else:
            return content
            
    except Exception as e:
        print(f"❌ Gemini Error: {str(e)}")
        raise

def query_openai(prompt):
    """Query OpenAI GPT for form structure"""
    client = get_openai_client()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert form architect. Extract form structure from documents and return valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json_match.group(0)
        else:
            return content
            
    except Exception as e:
        print(f"❌ OpenAI Error: {str(e)}")
        raise

def parse_pdf(pdf_path):
    """Extract form structure from PDF using LLM"""
    print(f"📄 Reading PDF: {pdf_path}")
    
    # 1. Extract Text from PDF (pages 2-11 only)
    text_content = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"   Total pages in PDF: {total_pages}")
            
            # Extract pages 2-11 (index 1-10, since indexing starts at 0)
            start_page = min(1, total_pages - 1)  # Page 2 (index 1)
            end_page = min(11, total_pages)        # Page 11 (index 10)
            
            print(f"   Extracting pages {start_page + 1} to {end_page}...")
            
            for i in range(start_page, end_page):
                if i < len(pdf.pages):
                    page = pdf.pages[i]
                    text = page.extract_text()
                    if text:
                        text_content += f"\n--- Page {i + 1} ---\n{text}"
                        print(f"     Page {i + 1}: {len(text)} chars extracted")
    except Exception as e:
        print(f"❌ Error reading PDF: {str(e)}")
        raise
    
    if not text_content.strip():
        raise ValueError("❌ No text could be extracted from PDF. Is it a scanned/image PDF?")
    
    print(f"   Total text extracted: {len(text_content)} characters")
    
    # 2. Create intelligent prompt for LLM
    prompt = f"""
DOCUMENT CONTENT (Pages 2-11 of form):

{text_content}

---

TASK: You are an Expert Form Architect. Analyze this Inherited IRA Application form completely and extract ALL form fields.

CRITICAL INSTRUCTIONS FOR THIS FORM:
1. Extract EVERY field you see including:
   - Text input fields (Name parts, Account Numbers, SSN, Tax ID, etc.)
   - Date fields (with mm/dd/yyyy format)
   - Checkboxes (Traditional IRA, Roth IRA, Qualified plan, etc.)
   - Account instructions sections
   - Numbered sections (1. Most Recent Decedent's Information, 2. Account Instructions, etc.)
   - Text input areas for account numbers
   - Radio button groups
   - Any signature/date sections

2. For EACH field found, provide:
   - id: unique lowercase_with_underscores identifier
   - label: exact label as shown (e.g., "Name First", "Social Security/Tax ID Number")
   - type: [text, email, phone, number, date, checkbox, radio, dropdown, textarea, file, currency, percentage]
   - required: boolean (true if mandatory or marked with *)
   - options: array of choices (for checkboxes: checkbox option text, for radio: all button options)
   - placeholder: hint text if visible (e.g., "mm/dd/yyyy" for dates)
   - validation: any rules mentioned (e.g., "numeric only", "must be same type")
   - visible_when: conditional visibility (null if always visible)
   - section: which form section this belongs to

3. Identify section structure and conditional logic

4. Return ONLY this JSON structure:

{{
    "formTitle": "Inherited IRA Application for Individual Beneficiaries",
    "formDescription": "Application for inheriting IRA accounts",
    "totalFields": number,
    "sections": [
        {{
            "name": "Section name",
            "fields": [fields list]
        }}
    ],
    "fields": [
        {{
            "id": "deceased_first_name",
            "label": "Name First",
            "type": "text",
            "required": true,
            "section": "1. Most Recent Decedent's Information",
            "placeholder": null,
            "options": [],
            "validation": null,
            "visible_when": null
        }},
        {{
            "id": "account_type_traditional_ira",
            "label": "Traditional IRA (includes Rollover, SEP, SIMPLE, and Inherited Traditional IRA)",
            "type": "checkbox",
            "required": false,
            "section": "1. Most Recent Decedent's Information",
            "options": ["Traditional IRA"],
            "validation": null,
            "visible_when": null
        }}
    ],
    "conditionalRules": [],
    "notes": "Form structure notes"
}}

CRITICAL REQUIREMENTS:
- Return ONLY valid JSON, no markdown, no text before/after
- Include ALL visible fields from the pages
- Don't miss checkboxes, text inputs, or date fields
- Use exact labels from document
- Include section information for each field
"""
    
    # 3. Query LLM
    print(f"🤖 Calling {LLM_PROVIDER.upper()} LLM for form analysis...")
    try:
        json_response = query_llm(prompt)
        
        # Clean up JSON response - handle invalid escape sequences
        import re
        
        # Strategy: Replace all single backslashes with proper JSON escaping
        # First, protect valid escape sequences
        json_response = json_response.replace('\\n', '\x00NEWLINE\x00')
        json_response = json_response.replace('\\t', '\x00TAB\x00')
        json_response = json_response.replace('\\r', '\x00RETURN\x00')
        json_response = json_response.replace('\\\\', '\x00BACKSLASH\x00')
        json_response = json_response.replace('\\"', '\x00QUOTE\x00')
        json_response = json_response.replace('\\/', '\x00SLASH\x00')
        
        # Remove all remaining backslashes (they're invalid)
        json_response = json_response.replace('\\', '')
        
        # Restore the protected sequences
        json_response = json_response.replace('\x00NEWLINE\x00', '\\n')
        json_response = json_response.replace('\x00TAB\x00', '\\t')
        json_response = json_response.replace('\x00RETURN\x00', '\\r')
        json_response = json_response.replace('\x00BACKSLASH\x00', '\\\\')
        json_response = json_response.replace('\x00QUOTE\x00', '\\"')
        json_response = json_response.replace('\x00SLASH\x00', '\\/')
        
        form_data = json.loads(json_response)
        
        print(f"✅ Form parsed successfully!")
        print(f"   Title: {form_data.get('formTitle', 'Unknown')}")
        print(f"   Fields found: {len(form_data.get('fields', []))}")
        
        # Show field summary
        fields = form_data.get('fields', [])
        if fields:
            print(f"\n   Field Summary:")
            for field in fields[:5]:  # Show first 5 fields
                print(f"     - {field.get('label')}: {field.get('type')}")
            if len(fields) > 5:
                print(f"     ... and {len(fields) - 5} more fields")
        
        return form_data
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON from LLM: {str(e)}")
        print(f"Raw response (first 1000 chars): {json_response[:1000]}")
        # Try to extract just the fields array if full JSON fails
        try:
            json_match = re.search(r'\{.*\}', json_response, re.DOTALL)
            if json_match:
                cleaned = json_match.group(0)
                # Remove any problematic characters
                cleaned = cleaned.encode('utf-8', 'ignore').decode('utf-8')
                form_data = json.loads(cleaned)
                print("✅ Recovered form data from partially valid JSON")
                return form_data
        except:
            pass
        raise
    except Exception as e:
        print(f"❌ LLM Processing Error: {str(e)}")
        raise

if __name__ == "__main__":
    # Get PDF file path from command line argument or use default
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
    else:
        pdf_file = "form.pdf"
    
    # Check if file exists
    if not os.path.exists(pdf_file):
        print(f"❌ Error: File '{pdf_file}' not found!")
        print(f"\n📝 Usage: python3 agent_parser.py <pdf_file>")
        print(f"   Example: python3 agent_parser.py myform.pdf")
        
        # Create a demo PDF if no file provided
        if pdf_file == "form.pdf":
            print(f"\n📌 Creating demo PDF: {pdf_file}")
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.pdfgen import canvas
                
                c = canvas.Canvas(pdf_file, pagesize=letter)
                c.drawString(50, 750, "Contact Form")
                c.drawString(50, 720, "First Name: ___________________")
                c.drawString(50, 690, "Email Address: ___________________")
                c.drawString(50, 660, "☐ Subscribe to Newsletter?")
                c.drawString(50, 630, "Reason for Contact: ___________________")
                c.drawString(100, 600, "☐ Support  ☐ Sales  ☐ Other")
                c.save()
                print(f"✅ Demo PDF created: {pdf_file}")
            except ImportError:
                print("⚠️ reportlab not installed. Install with: pip install reportlab")
                exit(1)
        else:
            exit(1)
    
    print(f"\n📄 Processing: {pdf_file}")
    form_data = parse_pdf(pdf_file)
    
    # Generate output filename based on input PDF
    output_file = os.path.splitext(pdf_file)[0] + "_form.json"
    
    with open(output_file, "w") as f:
        json.dump(form_data, f, indent=4)
    print(f"✅ Agent 1: PDF converted to {output_file}")