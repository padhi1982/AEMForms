"""
AEM Forms Agent Workflow - Web Interface
Orchestrates 3 agents: Parser → Builder → Mapper
"""
import os
import json
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import sys
from pathlib import Path

# Import configuration
from config import ensure_api_key, get_config

# Ensure API key is configured
print("\n🔧 Checking LLM configuration...")
ensure_api_key()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_workflow(pdf_path, base_name):
    """Run all 3 agents sequentially"""
    original_cwd = os.getcwd()
    output_dir = None
    
    try:
        results = {}
        
        # Create output directory
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], base_name)
        os.makedirs(output_dir, exist_ok=True)
        
        # Copy PDF to output directory
        import shutil
        input_pdf = os.path.join(output_dir, 'input.pdf')
        shutil.copy(pdf_path, input_pdf)
        print(f"[Agent 1] Parsing PDF: {input_pdf}")
        
        # Agent 1: Parser (PDF → JSON)
        try:
            from agent_parser import parse_pdf
            form_data = parse_pdf(input_pdf)
            
            json_path = os.path.join(output_dir, 'headless_form.json')
            with open(json_path, 'w') as f:
                json.dump(form_data, f, indent=4)
            results['json'] = form_data
            print("✅ Agent 1: PDF parsed to JSON")
        except Exception as e:
            raise Exception(f"Agent 1 (Parser) failed: {str(e)}")
        
        # Agent 2: Builder (JSON → HTML)
        try:
            print("[Agent 2] Building HTML form")
            
            # Read the JSON that was created
            json_path = os.path.join(output_dir, 'headless_form.json')
            with open(json_path, 'r') as f:
                form_data = json.load(f)
            
            # Build HTML manually (inline to avoid file path issues)
            from jinja2 import Template
            
            html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ formTitle }}</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .field { margin-bottom: 15px; }
            .hidden { display: none; }
            label { display: block; font-weight: bold; margin-bottom: 5px; }
            input, select { padding: 8px; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>{{ formTitle }}</h1>
        <form id="myAgentForm">
            {% for field in fields %}
            <div class="field" id="container_{{ field.id }}" data-rule="{{ field.visible_when }}">
                <label>{{ field.label }}</label>
                
                {% if field.type == 'text' or field.type == 'email' %}
                    <input type="{{ field.type }}" id="{{ field.id }}" name="{{ field.id }}" {% if field.required %}required{% endif %}>
                
                {% elif field.type == 'checkbox' %}
                    <input type="checkbox" id="{{ field.id }}" name="{{ field.id }}">
                
                {% elif field.type == 'dropdown' %}
                    <select id="{{ field.id }}" name="{{ field.id }}" {% if field.required %}required{% endif %}>
                        <option value="">Select an option</option>
                        {% for opt in field.options %}
                        <option value="{{ opt }}">{{ opt }}</option>
                        {% endfor %}
                    </select>
                {% endif %}
            </div>
            {% endfor %}
        </form>

        <script>
            const fields = document.querySelectorAll('.field');
            const inputs = document.querySelectorAll('input, select');

            function checkRules() {
                inputs.forEach(input => {
                    window[input.id] = input.type === 'checkbox' ? input.checked : input.value;
                });

                fields.forEach(field => {
                    const rule = field.dataset.rule;
                    if (rule && rule !== 'None' && rule !== '') {
                        try {
                            const isVisible = eval(rule); 
                            field.classList.toggle('hidden', !isVisible);
                        } catch(e) {
                            console.log('Rule error:', e);
                        }
                    }
                });
            }

            inputs.forEach(input => input.addEventListener('change', checkRules));
            checkRules();
        </script>
    </body>
    </html>
            """
            
            template = Template(html_template)
            html_output = template.render(form_data)
            
            html_path = os.path.join(output_dir, 'index.html')
            with open(html_path, 'w') as f:
                f.write(html_output)
            
            results['html'] = html_output
            print("✅ Agent 2: HTML form generated")
        except Exception as e:
            raise Exception(f"Agent 2 (Builder) failed: {str(e)}")
        
        # Agent 3: Mapper (HTML → AEM Spec)
        try:
            print("[Agent 3] Mapping to AEM specification")
            from bs4 import BeautifulSoup
            
            # Read the HTML
            html_path = os.path.join(output_dir, 'index.html')
            with open(html_path, 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            AEM_COMPONENT_MAP = {
                "text": "core/wcm/components/form/text",
                "email": "core/wcm/components/form/text (validation=email)",
                "checkbox": "core/wcm/components/form/options (type=checkbox)",
                "select": "core/wcm/components/form/options (type=drop-down)",
                "file": "core/wcm/components/form/upload"
            }
            
            aem_spec = {
                "target_container": "/content/forms/af/my-headless-form",
                "components_to_create": []
            }
            
            form = soup.find("form")
            if form:
                for input_tag in form.find_all(["input", "select"]):
                    field_type = input_tag.name if input_tag.name == "select" else input_tag.get("type", "text")
                    field_id = input_tag.get("id")
                    
                    aem_component = AEM_COMPONENT_MAP.get(field_type, "core/wcm/components/form/text")
                    
                    aem_spec["components_to_create"].append({
                        "field_id": field_id,
                        "html_origin": f"<{input_tag.name} type='{field_type}'>",
                        "aem_resource_type": aem_component,
                        "status": "Ready for JCR content creation"
                    })
            
            aem_path = os.path.join(output_dir, 'aem_spec_sheet.json')
            with open(aem_path, 'w') as f:
                json.dump(aem_spec, f, indent=4)
            
            results['aem_spec'] = aem_spec
            print("✅ Agent 3: AEM spec generated")
        except Exception as e:
            raise Exception(f"Agent 3 (Mapper) failed: {str(e)}")
        
        return results, None
        
    except Exception as e:
        error_msg = f"Workflow Error: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return None, error_msg
    finally:
        # Make sure we're back in original directory
        os.chdir(original_cwd)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle PDF file upload and run workflow"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        base_name = filename.rsplit('.', 1)[0]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Run workflow
        results, error = process_workflow(filepath, base_name)
        
        if error:
            return jsonify({'error': error}), 500
        
        return jsonify({
            'success': True,
            'message': 'Workflow completed successfully',
            'data': {
                'json': results['json'],
                'html': results['html'],
                'aem_spec': results['aem_spec'],
                'base_name': base_name
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/download/<path:filename>')
def download_file(filename):
    """Download generated files"""
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/preview-html/<base_name>')
def preview_html(base_name):
    """Preview the generated HTML form"""
    html_path = os.path.join(app.config['OUTPUT_FOLDER'], base_name, 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r') as f:
            return f.read()
    return "HTML not found", 404

if __name__ == '__main__':
    print("🚀 Starting AEM Forms Agent Workflow GUI...")
    print("📱 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, port=5000, host='localhost')
