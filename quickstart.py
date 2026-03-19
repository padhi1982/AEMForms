#!/usr/bin/env python3
"""
Quick start - Check configuration and start app
"""
import os
import sys
import json
from pathlib import Path

CONFIG_FILE = Path.home() / '.aem_forms_config.json'

def print_header():
    print("\n" + "="*70)
    print("🚀 AEM Forms Agent Workflow - Quick Start")
    print("="*70)

def check_config():
    """Check current configuration"""
    print("\n🔍 Checking configuration...\n")
    
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    
    google_key = config.get('google_api_key') or os.getenv('GOOGLE_API_KEY')
    openai_key = config.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
    
    llm_provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
    
    if google_key:
        print(f"✅ Google Gemini API: Configured")
        print(f"   Key: {google_key[:20]}...")
    else:
        print(f"⚠️  Google Gemini API: Not configured")
    
    if openai_key:
        print(f"✅ OpenAI API: Configured")
        print(f"   Key: {openai_key[:20]}...")
    else:
        print(f"⚠️  OpenAI API: Not configured")
    
    print(f"\n📌 Current LLM Provider: {llm_provider.upper()}")
    
    return {
        'has_google': bool(google_key),
        'has_openai': bool(openai_key),
        'provider': llm_provider
    }

def setup_gemini_interactive():
    """Setup Gemini with user input"""
    print("\n" + "-"*70)
    print("🆓 Setting up Google Gemini (FREE - No credit card needed)")
    print("-"*70)
    print("\n📝 To get your FREE API key:")
    print("   1. Open: https://ai.google.dev/")
    print("   2. Click 'Get API Key'")
    print("   3. Copy the key\n")
    
    import getpass
    api_key = getpass.getpass("🔑 Paste your Google API key: ").strip()
    
    if not api_key:
        print("❌ Cancelled")
        return False
    
    # Save
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    
    config['google_api_key'] = api_key
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    os.chmod(CONFIG_FILE, 0o600)
    os.environ['GOOGLE_API_KEY'] = api_key
    
    # Validate
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        genai.list_models()
        print("✅ Google Gemini API configured successfully!")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {str(e)}")
        return False

def main():
    print_header()
    
    config = check_config()
    
    # If no Gemini key but has OpenAI, suggest setting Gemini
    if not config['has_google'] and config['has_openai']:
        print("\n💡 Tip: You can also add Google Gemini (FREE) for redundancy")
        setup = input("\nSetup Google Gemini now? (y/n): ").lower()
        if setup == 'y':
            setup_gemini_interactive()
    
    # Ensure at least one provider is configured
    if not config['has_google'] and not config['has_openai']:
        print("\n❌ No LLM provider configured!")
        print("Please setup an API key first:")
        print("   python3 setup_gemini_simple.py")
        return False
    
    print("\n" + "="*70)
    print("✅ Configuration ready! Starting application...")
    print("="*70)
    print("\n🌐 Application will start on: http://localhost:5000")
    print("\nStarting Flask server...")
    print("="*70 + "\n")
    
    # Import and run app
    try:
        from app import app
        app.run(debug=True, port=5000, host='localhost')
    except Exception as e:
        print(f"❌ Error starting app: {str(e)}")
        return False

if __name__ == "__main__":
    main()
