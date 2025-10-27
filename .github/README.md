# GitHub Actions Setup for Currency Bot

This document explains how to set up automated currency monitoring using GitHub Actions.

## 🚀 Quick Setup

### 1. Prerequisites
- GitHub CLI (`gh`) installed and authenticated
- Gmail account with App Password enabled
- Repository with GitHub Actions enabled

### 2. Set Up Secrets
```bash
# Run the interactive setup script
./scripts/setup-github-secrets.sh setup
```

### 3. Test the Workflow
```bash
# Trigger a manual test run
./scripts/setup-github-secrets.sh test
```

## 📋 Required GitHub Secrets

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `CURRENCY_NOTIFICATION_EMAIL` | Gmail address for sending notifications | `your-email@gmail.com` |
| `CURRENCY_GMAIL_APP_PASSWORD` | Gmail App Password (not regular password) | `abcd efgh ijkl mnop` |
| `CURRENCY_RECIPIENT_EMAILS` | Comma-separated recipient emails | `user1@example.com,user2@example.com` |
| `CAD_RMB_THRESHOLD` | Exchange rate threshold | `5.05` |

## 🔧 Gmail App Password Setup

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" as the app
   - Copy the generated password (format: `abcd efgh ijkl mnop`)

## ⏰ Workflow Schedule

The currency monitoring workflow runs:
- **Automatically**: Every hour at the top of the hour
- **Manually**: Via GitHub Actions UI or CLI

## 📊 Workflow Jobs

### 1. Monitor CAD-RMB Rate
- Fetches current CAD-RMB exchange rate
- Compares against threshold
- **Smart Notifications**:
  - Sends ONE alert per day when rate drops below threshold
  - Sends daily summary at midnight when rate is above threshold
  - Prevents email spam with intelligent timing
- Uploads monitoring logs as artifacts

### 2. Health Check
- Tests all bot components
- Verifies API connectivity
- Ensures modules import correctly

### 3. Notify on Failure
- Sends notifications if monitoring fails
- Provides links to failed workflow runs

## 🛠️ Management Commands

```bash
# List current secrets
./scripts/setup-github-secrets.sh list

# Verify secrets are set correctly
./scripts/setup-github-secrets.sh verify

# Test the workflow manually
./scripts/setup-github-secrets.sh test

# Delete all secrets (if needed)
./scripts/setup-github-secrets.sh delete
```

## 📈 Monitoring Results

### Success Indicators
- ✅ Workflow completes without errors
- ✅ Email notifications sent when threshold breached
- ✅ Logs uploaded as artifacts
- ✅ Health check passes

### Failure Indicators
- ❌ Workflow fails with errors
- ❌ API connectivity issues
- ❌ Email sending failures
- ❌ Missing or invalid secrets

## 🧠 Smart Notification System

The currency bot uses an intelligent notification system to prevent email spam:

### Alert Notifications (Rate Below Threshold)
- **Trigger**: When CAD-RMB rate drops below threshold
- **Frequency**: Maximum ONE alert per day
- **Reset**: Daily flags reset at midnight
- **Purpose**: Immediate trading opportunity alerts

### Daily Summary (Rate Above Threshold)
- **Trigger**: When CAD-RMB rate is above threshold
- **Frequency**: Once daily at midnight (00:00)
- **Purpose**: Keep recipients informed without spam

### Benefits
- **No Spam**: Prevents overwhelming recipients with emails
- **Important Alerts**: Still get immediate notification for trading opportunities
- **Daily Updates**: Stay informed with regular market summaries
- **Smart Timing**: Alerts when needed, summaries at convenient times

## 🔍 Troubleshooting

### Common Issues

**Workflow Fails Immediately**
- Check that all required secrets are set
- Verify Gmail App Password is correct
- Ensure 2FA is enabled on Gmail account

**No Email Notifications**
- Verify recipient emails are valid
- Check Gmail App Password format
- Ensure firewall allows SMTP connections

**API Rate Limits**
- Free tier allows 1,500 requests/month
- Consider upgrading to paid tier
- Monitor usage in workflow logs

### Getting Help

1. **Check Workflow Logs**: Go to Actions tab in GitHub
2. **Verify Secrets**: Run `./scripts/setup-github-secrets.sh verify`
3. **Test Locally**: Run `python3 test_currency_bot.py`
4. **Manual Trigger**: Use GitHub Actions UI to trigger workflow

## 🔒 Security Notes

- All credentials are stored as encrypted GitHub Secrets
- Secrets are only accessible to repository collaborators
- Gmail App Passwords are more secure than regular passwords
- Workflow runs in isolated GitHub Actions environment

## 📝 Customization

### Change Monitoring Frequency
Edit `.github/workflows/periodic-monitoring.yml`:
```yaml
schedule:
  # Run every 30 minutes
  - cron: "0,30 * * * *"
```

### Modify Threshold
Update the `CAD_RMB_THRESHOLD` secret or modify the workflow to use a different value.

### Add More Currency Pairs
Extend the workflow to monitor additional currency pairs by adding new jobs.
