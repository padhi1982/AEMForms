#!/bin/bash
# 
# AEM Forms Agent Workflow - GitHub Publishing Commands
# Copy and paste these commands to publish your project
#

echo "╔════════════════════════════════════════════════════════╗"
echo "║   AEM Forms - GitHub Publishing Command Reference     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

echo "📝 STEP 1: Create Repository on GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Visit: https://github.com/new"
echo "  • Name: AEMforms"
echo "  • Visibility: Public"
echo "  • Description: AEM Forms Agent Workflow"
echo ""

echo "🔑 STEP 2: Push Code to GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Navigate to project"
echo "cd /Users/hargovindpadhi/Tools/PDF-AEMforms"
echo ""
echo "# Rename branch to main"
echo "git branch -M main"
echo ""
echo "# Add remote (use your URL from GitHub)"
echo "git remote add origin https://github.com/padhi1982/AEMforms.git"
echo ""
echo "# Push to GitHub"
echo "git push -u origin main"
echo ""

echo "🌐 STEP 3: Enable GitHub Pages"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Visit: https://github.com/padhi1982/AEMforms/settings/pages"
echo "  1. Source: Deploy from a branch"
echo "  2. Branch: main"
echo "  3. Folder: / (root)"
echo "  4. Click 'Save'"
echo ""
echo "Wait 1-2 minutes for deployment..."
echo ""

echo "✅ DONE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Your project will be live at:"
echo "  📱 https://padhi1982.github.io/AEMforms/"
echo "  💻 https://github.com/padhi1982/AEMforms"
echo ""
