#!/usr/bin/env python3
"""
Common Notification Manager Base Class
Shared notification functionality for currency monitors
"""

import logging
import smtplib
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict

from common.config.base_config import BaseConfig


class BaseNotificationManager(ABC):
    """Base notification manager for currency exchange rate alerts"""

    def __init__(self, config: BaseConfig):
        self.config = config
        self.notification_config = config.get_notification_config()
        self.logger = self._setup_logger()
        self.sent_notifications: set = set()
        self.alert_sent_today: bool = False
        self.last_daily_summary: str = ""

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for notifications"""
        logger = logging.getLogger(
            f"{self.config.currency_pair.lower().replace('-', '_')}_notifications"
        )
        logger.setLevel(logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)

        # Add handler
        logger.addHandler(console_handler)

        return logger

    def send_notifications(self, rate_data: Dict[str, Any]) -> bool:
        """Send notifications for currency rate alerts with smart spam prevention"""
        try:
            if not rate_data:
                self.logger.info("No rate data to notify about")
                return True

            current_rate = rate_data.get("current_rate")
            threshold = rate_data.get("threshold")

            if current_rate is None or threshold is None:
                self.logger.error("Missing required rate data")
                return False

            # Check if we should send an alert
            should_send_alert = self._should_send_alert(current_rate, threshold)

            if should_send_alert:
                self.logger.info(
                    f"Sending alert for {self.config.currency_pair} rate: {current_rate} (threshold: {threshold})"
                )

                # Send immediate alert
                alert_sent = self._send_email_notification(rate_data, is_alert=True)

                if alert_sent:
                    self.alert_sent_today = True
                    self.last_daily_summary = ""  # Reset daily summary flag

                return alert_sent
            else:
                # Check if we should send daily summary
                should_send_summary = self._should_send_daily_summary(
                    current_rate, threshold
                )

                if should_send_summary:
                    self.logger.info(
                        f"Sending daily summary for {self.config.currency_pair} rate: {current_rate}"
                    )

                    # Send daily summary
                    summary_sent = self._send_email_notification(
                        rate_data, is_alert=False
                    )

                    if summary_sent:
                        self.last_daily_summary = self._get_today_date()

                    return summary_sent
                else:
                    self.logger.info(
                        f"No notification needed for {self.config.currency_pair} rate: {current_rate}"
                    )
                    return True

        except Exception as e:
            self.logger.error(f"Error sending notifications: {e}")
            return False

    def _should_send_alert(self, current_rate: float, threshold: float) -> bool:
        """Determine if we should send an immediate alert"""
        # Send alert if rate is below threshold AND we haven't sent an alert today
        return current_rate < threshold and not self.alert_sent_today

    def _should_send_daily_summary(self, current_rate: float, threshold: float) -> bool:
        """Determine if we should send a daily summary"""
        from datetime import datetime

        today = self._get_today_date()

        # Send daily summary if:
        # 1. We haven't sent a summary today
        # 2. It's been 24 hours since last summary
        # 3. Rate is above threshold (no active alert)
        return (
            self.last_daily_summary != today
            and current_rate >= threshold
            and self._is_time_for_daily_summary()
        )

    def _get_today_date(self) -> str:
        """Get today's date as string"""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d")

    def _is_time_for_daily_summary(self) -> bool:
        """Check if it's time for daily summary (every 24 hours)"""
        from datetime import datetime

        # Reset daily flags at midnight
        current_hour = datetime.now().hour
        return current_hour == 0  # Send at midnight

    def reset_daily_flags(self):
        """Reset daily notification flags (call at midnight)"""
        from datetime import datetime

        today = self._get_today_date()

        # Reset flags if it's a new day
        if self.last_daily_summary != today:
            self.alert_sent_today = False
            self.last_daily_summary = ""
            self.logger.info("Daily notification flags reset for new day")

    def _send_email_notification(
        self, rate_data: Dict[str, Any], is_alert: bool = True
    ) -> bool:
        """Send email notification for currency rate alert"""
        try:
            sender_email = self.notification_config.get("email")
            gmail_password = self.notification_config.get("gmail_app_password")
            recipient_emails = self.notification_config.get(
                "recipient_emails", sender_email
            )

            if not sender_email or not gmail_password:
                self.logger.warning(
                    "Email credentials not configured, skipping email notification"
                )
                return True

            # Parse recipient emails (comma-separated string or single email)
            if isinstance(recipient_emails, str):
                if "," in recipient_emails:
                    recipients = [
                        email.strip()
                        for email in recipient_emails.split(",")
                        if email.strip()
                    ]
                else:
                    recipients = [recipient_emails.strip()]
            else:
                recipients = [sender_email]  # Fallback to sender

            # Create message based on type
            if is_alert:
                subject = f"🚨 {self.config.currency_pair} Exchange Rate Alert!"
            else:
                subject = f"📊 {self.config.currency_pair} Daily Summary"

            body = self._format_email_message(rate_data, is_alert=is_alert)

            # Create email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "html"))

            # Send email
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, gmail_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipients, text)
            server.quit()

            self.logger.info(
                f"{self.config.currency_pair} email notification sent successfully to {len(recipients)} recipient(s): {', '.join(recipients)}"
            )
            return True

        except Exception as e:
            self.logger.error(
                f"Error sending {self.config.currency_pair} email notification: {e}"
            )
            return False

    @abstractmethod
    def _format_email_message(
        self, rate_data: Dict[str, Any], is_alert: bool = True
    ) -> str:
        """Format email message for currency rate alert or summary"""
        pass

    def send_test_notification(self) -> bool:
        """Send a test notification to verify configuration"""
        try:
            # Create test rate data
            test_rate_data = {
                "current_rate": 5.02,
                "threshold": 5.05,
                "timestamp": "2025-01-27T10:00:00",
                "currency_pair": self.config.currency_pair,
            }

            self.logger.info(
                f"Sending test {self.config.currency_pair} notification..."
            )
            return self.send_notifications(test_rate_data)

        except Exception as e:
            self.logger.error(
                f"Error sending test {self.config.currency_pair} notification: {e}"
            )
            return False
