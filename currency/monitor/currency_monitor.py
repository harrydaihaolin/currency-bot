#!/usr/bin/env python3
"""
Currency Monitor
Monitor for RMB-CAD currency exchange rate
"""

from typing import Any, Dict, Optional

from common.monitor.base_monitor import BaseMonitor
from currency.config.currency_config import CurrencyConfig


class CurrencyMonitor(BaseMonitor):
    """Monitor for RMB-CAD exchange rate"""

    def __init__(self, config: CurrencyConfig):
        super().__init__(config)
        self.base_currency = config.get_api_config()["base_currency"]
        self.target_currency = config.get_api_config()["target_currency"]

    def _extract_rate_from_response(self, data: Dict[str, Any]) -> Optional[float]:
        """Extract CAD-RMB exchange rate from API response"""
        try:
            # The API returns rates in the format: 1 CAD = X CNY
            # So we need to get the CNY rate from CAD
            rates = data.get("rates", {})
            cny_rate = rates.get(self.target_currency)
            
            if cny_rate is None:
                self.logger.error(f"Could not find {self.target_currency} rate in response")
                return None
            
            # Convert to CAD-RMB rate (1 CAD = X RMB)
            # Since CAD is the base currency, the rate is already CAD-RMB
            return float(cny_rate)
            
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error(f"Error extracting rate from response: {e}")
            return None

    def get_rate_info(self) -> Optional[Dict[str, Any]]:
        """Get detailed rate information"""
        try:
            api_url = self.api_config["api_url"]
            api_key = self.api_config.get("api_key")
            
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            import requests
            response = requests.get(
                api_url,
                headers=headers,
                timeout=self.monitoring_config["timeout"]
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "base_currency": data.get("base", self.base_currency),
                "date": data.get("date"),
                "rates": data.get("rates", {}),
                "target_rate": self._extract_rate_from_response(data)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting rate info: {e}")
            return None
