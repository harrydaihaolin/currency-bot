# 💱 RMB-CAD Currency Exchange Rate Monitor 💱

An automated bot that monitors the RMB-CAD exchange rate and sends email notifications when the rate drops below a specified threshold.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Set Up Configuration
```bash
# Copy environment template
cp env.example .env

# Edit configuration
nano .env
```

### 3. Start Monitoring

#### Option A: Local Daemon (Recommended)
```bash
# One-command daemon experience
./scripts/run_daemon.sh start

# Check status
./scripts/run_daemon.sh status

# Stop daemon
./scripts/run_daemon.sh stop
```

#### Option B: Docker (Alternative)
```bash
# One-command Docker experience
./scripts/docker-manage.sh start

# Check status
./scripts/docker-manage.sh status

# View logs
./scripts/docker-manage.sh logs

# Stop container
./scripts/docker-manage.sh stop
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with your configuration:

```bash
# RMB-CAD Exchange Rate Monitoring
RMB_CAD_MONITORING_INTERVAL=60  # minutes (default: 60)
RMB_CAD_THRESHOLD=5.05  # exchange rate threshold (default: 5.05)
RMB_CAD_MAX_ATTEMPTS=3  # max API retry attempts (default: 3)
RMB_CAD_TIMEOUT=30  # API timeout in seconds (default: 30)
RMB_CAD_LOG_FILE=rmb_cad_monitoring.log  # log file name
RMB_CAD_LOG_LEVEL=INFO  # log level (DEBUG, INFO, WARNING, ERROR)

# Exchange Rate API Configuration
EXCHANGE_API_KEY=  # Optional API key for exchangerate-api.com (free tier works without key)

# Email Notification Configuration
CURRENCY_NOTIFICATION_EMAIL=your_email@gmail.com
CURRENCY_GMAIL_APP_PASSWORD=your_gmail_app_password
CURRENCY_RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com
```

### Gmail App Password
To send email notifications, you need a Gmail App Password:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password for "Mail"
3. Use this password in `CURRENCY_GMAIL_APP_PASSWORD`

## 📋 Features

- **Real-time Monitoring**: Tracks RMB-CAD exchange rate every hour (configurable)
- **Email Notifications**: Instant alerts when rate drops below threshold
- **Configurable Thresholds**: Set your own exchange rate alert level
- **Docker Support**: Easy containerized deployment
- **Daemon Mode**: Background monitoring with process management
- **Robust Error Handling**: Automatic retries and graceful failure handling
- **Comprehensive Logging**: Detailed logs for monitoring and debugging

## 🛠️ Management Commands

### Docker Management
```bash
./scripts/docker-manage.sh start     # Start container
./scripts/docker-manage.sh stop       # Stop container
./scripts/docker-manage.sh restart    # Restart container
./scripts/docker-manage.sh logs      # View logs
./scripts/docker-manage.sh status    # Check status
./scripts/docker-manage.sh build     # Rebuild container
```

### Daemon Management
```bash
./scripts/run_daemon.sh start [interval]  # Start daemon monitoring
./scripts/run_daemon.sh stop              # Stop daemon
./scripts/run_daemon.sh restart [interval] # Restart daemon
./scripts/run_daemon.sh status            # Check daemon status
./scripts/run_daemon.sh logs              # View daemon logs
```

## 📁 Project Structure

```
currency-bot/
├── currency/                    # Currency-specific modules
│   ├── config/                 # Currency configuration
│   ├── monitor/                # Currency monitoring logic
│   └── notifications/          # Currency notification formatting
├── common/                     # Shared modules
│   ├── config/                # Base configuration classes
│   ├── monitor/               # Base monitoring classes
│   └── notifications/         # Base notification classes
├── scripts/                   # Utility scripts
│   ├── docker-manage.sh       # Docker management
│   └── run_daemon.sh          # Daemon management
├── tests/                     # Unit tests
├── currency_bot.py            # Main bot entry point
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image definition
├── requirements.txt           # Python dependencies
└── env.example               # Environment configuration template
```

## 🧪 Testing

```bash
# Run the bot in test mode
python3 currency_bot.py

# Test email notifications
python3 -c "
from currency.config.currency_config import CurrencyConfig
from currency.notifications.currency_notifications import CurrencyNotificationManager
config = CurrencyConfig()
notifications = CurrencyNotificationManager(config)
notifications.send_test_notification()
"
```

## 🔄 Automated Monitoring

The bot can run automatically in various environments:

### GitHub Actions (Recommended)
- **Automated**: Runs every hour via GitHub Actions
- **Cloud-based**: No local resources required
- **Secure**: Credentials stored as encrypted secrets
- **Reliable**: GitHub's infrastructure with automatic retries
- **Free**: No additional hosting costs

```bash
# Set up GitHub Actions monitoring
./scripts/setup-github-secrets.sh setup
./scripts/setup-github-secrets.sh test
```

### Local Daemon
- Runs continuously in the background
- Automatically restarts on failure
- Configurable monitoring intervals
- Comprehensive logging

### Docker Container
- Containerized deployment
- Health checks and automatic restarts
- Volume mounting for persistent logs
- Easy scaling and management

## 🤖 GitHub Actions Setup

### Quick Start with GitHub Actions
```bash
# 1. Install GitHub CLI and authenticate
brew install gh  # macOS
gh auth login

# 2. Set up secrets interactively
./scripts/setup-github-secrets.sh setup

# 3. Test the workflow
./scripts/setup-github-secrets.sh test
```

### Required GitHub Secrets
- `CURRENCY_NOTIFICATION_EMAIL` - Your Gmail address
- `CURRENCY_GMAIL_APP_PASSWORD` - Gmail App Password (not regular password)
- `CURRENCY_RECIPIENT_EMAILS` - Comma-separated recipient emails
- `CAD_RMB_THRESHOLD` - Exchange rate threshold (default: 5.05)

### Workflow Features
- **Schedule**: Runs every hour automatically
- **Manual Trigger**: Can be triggered manually via GitHub UI
- **Health Checks**: Tests all components before monitoring
- **Log Artifacts**: Uploads monitoring logs for debugging
- **Failure Notifications**: Alerts on workflow failures

## 📊 Exchange Rate API

The bot uses the [exchangerate-api.com](https://exchangerate-api.com) service:
- **Free tier**: No API key required
- **Rate limits**: 1,500 requests/month (free tier)
- **Update frequency**: Real-time rates
- **Reliability**: High uptime and accuracy

## 📝 Version History

- **v1.0.0** - Initial Release
  - RMB-CAD exchange rate monitoring
  - Email notifications
  - Docker support
  - Daemon management
  - Configurable thresholds and intervals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Email Notifications Not Working**:
- Verify Gmail App Password is correct and 2FA is enabled
- Check that recipient emails are valid
- Ensure firewall allows SMTP connections

**API Rate Limits**:
- The free tier allows 1,500 requests/month
- Consider upgrading to paid tier for higher limits
- Monitor usage in logs

**Docker Issues**:
- Ensure Docker and Docker Compose are installed and running
- Check that .env file is properly configured
- Verify container logs for errors

**Daemon Issues**:
- Check daemon logs: `tail -f currency_daemon.log`
- Verify daemon status: `./scripts/run_daemon.sh status`
- Ensure proper permissions on script files

### Getting Help

- Check daemon logs: `tail -f currency_daemon.log`
- Check daemon status: `./scripts/run_daemon.sh status`
- View container logs: `./scripts/docker-manage.sh logs`
- Test configuration: Run bot in interactive mode

## 🔮 Future Enhancements

- Support for multiple currency pairs
- SMS notifications via Twilio
- Web dashboard for monitoring
- Historical rate tracking
- Advanced alerting rules
- Integration with trading platforms
