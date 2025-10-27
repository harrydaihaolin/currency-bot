#!/usr/bin/env python3
"""
Common Monitor Base Class
Shared monitoring functionality for currency exchange rate monitors
"""

import logging
import requests
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from common.config.base_config import BaseConfig


class BaseMonitor(ABC):
    """Base monitor for currency exchange rates"""

    def __init__(self, config: BaseConfig):
        self.config = config
        self.api_config = config.get_api_config()
        self.monitoring_config = config.get_monitoring_config()
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for monitoring"""
        logger = logging.getLogger(f"{self.config.currency_pair.lower().replace('-', '_')}_monitor")
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

    def get_current_rate(self) -> Optional[float]:
        """Get current exchange rate"""
        try:
            api_url = self.api_config["api_url"]
            api_key = self.api_config.get("api_key")
            
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            response = requests.get(
                api_url,
                headers=headers,
                timeout=self.monitoring_config["timeout"]
            )
            response.raise_for_status()
            
            data = response.json()
            return self._extract_rate_from_response(data)
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching exchange rate: {e}")
            return None

    @abstractmethod
    def _extract_rate_from_response(self, data: Dict[str, Any]) -> Optional[float]:
        """Extract exchange rate from API response"""
        pass

    def get_rate_with_retry(self, max_attempts: Optional[int] = None) -> Optional[float]:
        """Get exchange rate with retry logic"""
        if max_attempts is None:
            max_attempts = self.monitoring_config["max_attempts"]
        
        for attempt in range(max_attempts):
            try:
                rate = self.get_current_rate()
                if rate is not None:
                    return rate
                
                if attempt < max_attempts - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
        
        self.logger.error(f"Failed to get exchange rate after {max_attempts} attempts")
        return None
