#!/usr/bin/env python3
"""
Currency Notification Manager
Notification manager for RMB-CAD currency exchange rate alerts
"""

from datetime import datetime
from typing import Any, Dict

from common.notifications.base_notifications import BaseNotificationManager
from currency.config.currency_config import CurrencyConfig


class CurrencyNotificationManager(BaseNotificationManager):
    """Notification manager for RMB-CAD exchange rate alerts"""

    def __init__(self, config: CurrencyConfig):
        super().__init__(config)

    def _format_email_message(self, rate_data: Dict[str, Any], is_alert: bool = True) -> str:
        """Format email message for CAD-RMB rate alert or daily summary"""
        current_rate = rate_data.get("current_rate", 0)
        threshold = rate_data.get("threshold", 0)
        timestamp = rate_data.get("timestamp", datetime.now().isoformat())
        currency_pair = rate_data.get("currency_pair", "CAD-RMB")
        
        # Calculate the difference
        difference = current_rate - threshold
        percentage_change = (difference / threshold) * 100 if threshold > 0 else 0
        
        # Format timestamp for display
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            formatted_time = timestamp

        # Choose template based on type
        if is_alert:
            return self._format_alert_email(current_rate, threshold, difference, percentage_change, formatted_time, currency_pair)
        else:
            return self._format_summary_email(current_rate, threshold, difference, percentage_change, formatted_time, currency_pair)
    
    def _format_alert_email(self, current_rate: float, threshold: float, difference: float, percentage_change: float, formatted_time: str, currency_pair: str) -> str:
        """Format alert email (rate below threshold)"""
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #e74c3c; text-align: center;">
                    🚨 Currency Exchange Rate Alert
                </h2>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0;">
                        {currency_pair} Exchange Rate Alert
                    </h3>
                    
                    <div style="display: flex; justify-content: space-between; margin: 15px 0;">
                        <div style="text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #e74c3c;">
                                {current_rate:.4f}
                            </div>
                            <div style="color: #7f8c8d; font-size: 14px;">
                                Current Rate (1 CAD = X RMB)
                            </div>
                        </div>
                        
                        <div style="text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #27ae60;">
                                {threshold:.4f}
                            </div>
                            <div style="color: #7f8c8d; font-size: 14px;">
                                Alert Threshold
                            </div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="font-size: 18px; font-weight: bold; color: #e74c3c;">
                            Difference: {difference:+.4f} ({percentage_change:+.2f}%)
                        </div>
                    </div>
                </div>
                
                <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4 style="color: #856404; margin-top: 0;">
                        ⚠️ Alert Details
                    </h4>
                    <p style="margin: 5px 0; color: #856404;">
                        The {currency_pair} exchange rate has dropped below your specified threshold of {threshold:.4f}.
                    </p>
                    <p style="margin: 5px 0; color: #856404;">
                        Current rate: <strong>{current_rate:.4f}</strong> (1 CAD = {current_rate:.4f} RMB)
                    </p>
                    <p style="margin: 5px 0; color: #856404;">
                        Alert triggered at: <strong>{formatted_time}</strong>
                    </p>
                </div>
                
                <div style="background-color: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4 style="color: #0c5460; margin-top: 0;">
                        📊 What This Means
                    </h4>
                    <p style="margin: 5px 0; color: #0c5460;">
                        A lower CAD-RMB rate means that 1 Canadian Dollar can buy fewer Chinese Yuan (RMB).
                    </p>
                    <p style="margin: 5px 0; color: #0c5460;">
                        This could be a good time to exchange CAD for RMB if you're planning to make a purchase in China.
                    </p>
                </div>
                
                <div style="text-align: center; margin: 30px 0; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
                    <p style="color: #6c757d; font-size: 14px; margin: 0;">
                        This alert was generated by your Currency Exchange Rate Monitor
                    </p>
                    <p style="color: #6c757d; font-size: 12px; margin: 5px 0 0 0;">
                        Monitor ID: {currency_pair}-{datetime.now().strftime('%Y%m%d-%H%M%S')}
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def _format_summary_email(self, current_rate: float, threshold: float, difference: float, percentage_change: float, formatted_time: str, currency_pair: str) -> str:
        """Format daily summary email (rate above threshold)"""
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #27ae60; text-align: center;">
                    📊 Daily Currency Summary
                </h2>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #2c3e50; margin-top: 0;">
                        {currency_pair} Daily Summary
                    </h3>
                    
                    <div style="display: flex; justify-content: space-between; margin: 15px 0;">
                        <div style="text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #27ae60;">
                                {current_rate:.4f}
                            </div>
                            <div style="color: #7f8c8d; font-size: 14px;">
                                Current Rate (1 CAD = X RMB)
                            </div>
                        </div>
                        
                        <div style="text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #6c757d;">
                                {threshold:.4f}
                            </div>
                            <div style="color: #7f8c8d; font-size: 14px;">
                                Alert Threshold
                            </div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="font-size: 18px; font-weight: bold; color: #27ae60;">
                            Difference: {difference:+.4f} ({percentage_change:+.2f}%)
                        </div>
                    </div>
                </div>
                
                <div style="background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4 style="color: #155724; margin-top: 0;">
                        ✅ Status Update
                    </h4>
                    <p style="margin: 5px 0; color: #155724;">
                        The {currency_pair} exchange rate is currently <strong>above</strong> your alert threshold.
                    </p>
                    <p style="margin: 5px 0; color: #155724;">
                        Current rate: <strong>{current_rate:.4f}</strong> (1 CAD = {current_rate:.4f} RMB)
                    </p>
                    <p style="margin: 5px 0; color: #155724;">
                        Summary generated at: <strong>{formatted_time}</strong>
                    </p>
                </div>
                
                <div style="background-color: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4 style="color: #0c5460; margin-top: 0;">
                        📈 Market Analysis
                    </h4>
                    <p style="margin: 5px 0; color: #0c5460;">
                        The Canadian Dollar is performing well against the Chinese Yuan.
                    </p>
                    <p style="margin: 5px 0; color: #0c5460;">
                        No immediate trading opportunities detected. We'll continue monitoring and alert you if the rate drops below {threshold:.4f}.
                    </p>
                </div>
                
                <div style="text-align: center; margin: 30px 0; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
                    <p style="color: #6c757d; font-size: 14px; margin: 0;">
                        Daily summary from your Currency Exchange Rate Monitor
                    </p>
                    <p style="color: #6c757d; font-size: 12px; margin: 5px 0 0 0;">
                        Monitor ID: {currency_pair}-{datetime.now().strftime('%Y%m%d-%H%M%S')}
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_body
