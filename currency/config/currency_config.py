#!/usr/bin/env python3
"""
Currency Configuration
Configuration for RMB-CAD currency exchange rate monitoring
"""

import os
from typing import Dict

from common.config.base_config import BaseConfig


class CurrencyConfig(BaseConfig):
    """Configuration for RMB-CAD currency monitoring"""

    def __init__(self):
        super().__init__("CAD-RMB")
        self.api_url = "https://api.exchangerate-api.com/v4/latest/CAD"
        self.api_key = os.getenv("EXCHANGE_API_KEY", "")

    def get_api_config(self) -> Dict[str, str]:
        """Get API configuration"""
        return {
            "api_url": self.api_url,
            "api_key": self.api_key,
            "base_currency": "CAD",  # Canadian Dollar
            "target_currency": "CNY",  # Chinese Yuan (RMB)
        }

    def get_notification_config(self) -> Dict[str, str]:
        """Get notification configuration"""
        return {
            "email": os.getenv("CURRENCY_NOTIFICATION_EMAIL", ""),
            "gmail_app_password": os.getenv("CURRENCY_GMAIL_APP_PASSWORD", ""),
            "recipient_emails": os.getenv("CURRENCY_RECIPIENT_EMAILS", ""),
        }
