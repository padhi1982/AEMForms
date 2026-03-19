#!/usr/bin/env python3
"""
Simple Gemini API Key Setup
"""
import os
import json
import getpass
from pathlib import Path

CONFIG_FILE = Path.home() / '.aem_forms_config.json'

def setup_gemini():
    print("\n" + "="*70)
    print("🎉 AEM Forms Agent Workflow - Google Gemini Setup")
    print("="*70)
    print("\n✨ GOOD NEWS: Google Gemini is FREE and requires NO credit card!")
    print("\n📝 Follow these steps to get your FREE API key:\n")
    print("  1. Open: https://ai.google.dev/")
    print("  2. Click the 'Get API Key' button")
    print("  3. Select or create a Google Cloud project")
    print("  4. Copy your API key")
    print("\n" + "-"*70)
    
    # Get API key
    api_key = getpass.getpass("\n🔑 Paste your Google Gemini API key (won't be visible): ").strip()
    
    if not api_key:
        print("❌ API key cannot be empty!")
        return False
    
    if len(api_key) < 20:
        print("⚠️  Warning: API key seems too short")
    
    # Validate
    print("\n🔍 Validating API key...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Test with a simple call
        models = genai.list_models()
        model_count = sum(1 for _ in models)
        print(f"✅ API key is valid! Found {model_count} available models")
    except Exception as e:
        print(f"❌ Invalid API key: {str(e)}")
        return False
    
    # Save config
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    
    config['google_api_key'] = api_key
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    os.chmod(CONFIG_FILE, 0o600)
    os.environ['GOOGLE_API_KEY'] = api_key
    
    print(f"\n✅ Configuration saved to: {CONFIG_FILE}")
    print("   File permissions: 600 (secure)")
    
    return True

if __name__ == "__main__":
    if setup_gemini():
        print("\n" + "="*70)
        print("🎉 Setup Complete!")
        print("="*70)
        print("\n🚀 You can now start the application:")
        print("   python3 app.py")
        print("\n📱 Then open: http://localhost:5000")
        print("\n" + "="*70)
    else:
        print("\n❌ Setup failed. Please try again.")
        exit(1)
