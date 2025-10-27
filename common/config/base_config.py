#!/usr/bin/env python3
"""
Common Configuration Base Class
Shared configuration functionality for currency monitors
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseConfig(ABC):
    """Base configuration class for currency monitors"""

    def __init__(self, currency_pair: str):
        self.currency_pair = currency_pair
        self.api_url = ""
        self.api_key = ""

    @abstractmethod
    def get_api_config(self) -> Dict[str, str]:
        """Get API configuration"""
        pass

    @abstractmethod
    def get_notification_config(self) -> Dict[str, str]:
        """Get notification configuration"""
        pass

    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration"""
        prefix = self.currency_pair.replace("-", "_").upper()
        return {
            "monitoring_interval": int(
                os.getenv(f"{prefix}_MONITORING_INTERVAL", "60")
            ),  # minutes
            "threshold": float(
                os.getenv(f"{prefix}_THRESHOLD", "5.05")
            ),  # exchange rate threshold
            "max_attempts": int(
                os.getenv(f"{prefix}_MAX_ATTEMPTS", "3")
            ),  # max API retry attempts
            "timeout": int(os.getenv(f"{prefix}_TIMEOUT", "30")),  # seconds
        }

    def get_logging_config(self) -> Dict[str, str]:
        """Get logging configuration"""
        prefix = self.currency_pair.replace("-", "_").upper()
        return {
            "log_file": os.getenv(
                f"{prefix}_LOG_FILE", f"{self.currency_pair.lower().replace('-', '_')}_monitoring.log"
            ),
            "log_level": os.getenv(f"{prefix}_LOG_LEVEL", "INFO"),
            "log_format": "%(asctime)s - %(levelname)s - %(message)s",
        }

    def validate_config(self) -> bool:
        """Validate that all required configuration is present"""
        try:
            api_config = self.get_api_config()
            notif_config = self.get_notification_config()

            # Check API configuration
            if not api_config.get("api_url"):
                return False

            # Check notification configuration
            if not notif_config.get("email"):
                return False

            # If email is configured, check Gmail app password
            if notif_config.get("email") and not notif_config.get("gmail_app_password"):
                return False

            return True

        except Exception:
            return False
