#!/bin/bash
# GitHub Actions Setup Verification Script

echo "🔍 Verifying GitHub Actions Setup for Currency Bot"
echo "=================================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a Git repository!"
    echo "Please run: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

echo "✅ Git repository detected"

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed!"
    echo "Please install it first:"
    echo "  macOS: brew install gh"
    echo "  Ubuntu: sudo apt install gh"
    exit 1
fi

echo "✅ GitHub CLI is installed"

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub!"
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ Authenticated with GitHub"

# Check if workflow files exist
if [ ! -f ".github/workflows/periodic-monitoring.yml" ]; then
    echo "❌ Workflow file not found!"
    exit 1
fi

echo "✅ Workflow files exist"

# Check if secrets are set
echo ""
echo "📋 Checking GitHub Secrets..."
echo "=============================="

secrets_status=0

# Check required secrets
required_secrets=(
    "CURRENCY_NOTIFICATION_EMAIL"
    "CURRENCY_GMAIL_APP_PASSWORD"
    "CURRENCY_RECIPIENT_EMAILS"
    "CAD_RMB_THRESHOLD"
)

for secret in "${required_secrets[@]}"; do
    if gh secret list | grep -q "$secret"; then
        echo "✅ $secret is set"
    else
        echo "❌ $secret is missing"
        secrets_status=1
    fi
done

# Check optional secrets
if gh secret list | grep -q "EXCHANGE_API_KEY"; then
    echo "✅ EXCHANGE_API_KEY is set (optional)"
else
    echo "ℹ️  EXCHANGE_API_KEY is not set (optional - free tier works without)"
fi

echo ""
if [ $secrets_status -eq 0 ]; then
    echo "🎉 All required secrets are configured!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Push your code to GitHub:"
    echo "   git remote add origin <your-github-repo-url>"
    echo "   git push -u origin main"
    echo ""
    echo "2. Test the workflow:"
    echo "   ./scripts/setup-github-secrets.sh test"
    echo ""
    echo "3. Monitor the workflow:"
    echo "   gh run list"
    echo ""
    echo "4. View workflow logs:"
    echo "   gh run view <run-id>"
else
    echo "⚠️  Some secrets are missing!"
    echo ""
    echo "To set up secrets, run:"
    echo "   ./scripts/setup-github-secrets.sh setup"
fi

echo ""
echo "🔧 Workflow Configuration:"
echo "- Schedule: Every hour (0 * * * *)"
echo "- Manual trigger: Available via GitHub UI"
echo "- Smart notifications: Prevents email spam"
echo "- Recipients: harry442930583@gmail.com, mikoxyr@outlook.com"
echo "- Threshold: 5.05 CAD-RMB"
