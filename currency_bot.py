#!/usr/bin/env python3
"""
💱 RMB-CAD Currency Exchange Rate Monitor 💱

A specialized currency monitoring bot that tracks the RMB-CAD exchange rate
and sends email notifications when the rate drops below a specified threshold.
"""

import logging
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import currency-specific components
from currency.config.currency_config import CurrencyConfig
from currency.monitor.currency_monitor import CurrencyMonitor
from currency.notifications.currency_notifications import CurrencyNotificationManager


class CADRMBCurrencyBot:
    """CAD-RMB Currency Exchange Rate Monitor"""

    def __init__(self):
        self.config = CurrencyConfig()
        self.monitor = CurrencyMonitor(self.config)
        self.notifications = CurrencyNotificationManager(self.config)
        self.setup_logging()

    def setup_logging(self):
        """Set up logging configuration"""
        log_config = self.config.get_logging_config()
        logging.basicConfig(
            level=getattr(logging, log_config["log_level"]),
            format=log_config["log_format"],
            handlers=[
                logging.FileHandler(log_config["log_file"]),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def run_single_check(self):
        """Run a single currency rate check"""
        self.logger.info("🔍 Starting single currency rate check...")
        
        try:
            # Get current exchange rate
            current_rate = self.monitor.get_current_rate()
            
            if current_rate:
                self.logger.info(f"💱 Current CAD-RMB rate: {current_rate}")
                
                # Check if rate is below threshold
                threshold = self.config.get_monitoring_config()["threshold"]
                
                if current_rate < threshold:
                    self.logger.info(f"⚠️  Rate {current_rate} is below threshold {threshold}!")
                    
                    # Send notification
                    rate_data = {
                        "current_rate": current_rate,
                        "threshold": threshold,
                        "timestamp": datetime.now().isoformat(),
                        "currency_pair": "CAD-RMB"
                    }
                    
                    self.notifications.send_notifications(rate_data)
                    self.logger.info("📧 Alert notification sent!")
                else:
                    self.logger.info(f"✅ Rate {current_rate} is above threshold {threshold}")
            else:
                self.logger.error("❌ Failed to fetch current exchange rate")
                
        except Exception as e:
            self.logger.error(f"❌ Error during rate check: {e}")

    def run_continuous_monitoring(self):
        """Run continuous monitoring"""
        self.logger.info("🔄 Starting continuous currency monitoring...")
        
        try:
            monitoring_config = self.config.get_monitoring_config()
            interval = monitoring_config["monitoring_interval"]
            threshold = monitoring_config["threshold"]
            
            self.logger.info(f"⏰ Monitoring every {interval} minutes")
            self.logger.info(f"🎯 Alert threshold: {threshold}")
            
            while True:
                try:
                    # Reset daily flags at midnight
                    self.notifications.reset_daily_flags()
                    
                    # Get current exchange rate
                    current_rate = self.monitor.get_current_rate()
                    
                    if current_rate:
                        self.logger.info(f"💱 Current CAD-RMB rate: {current_rate}")
                        
                        # Send smart notifications (handles alerts and daily summaries)
                        rate_data = {
                            "current_rate": current_rate,
                            "threshold": threshold,
                            "timestamp": datetime.now().isoformat(),
                            "currency_pair": "CAD-RMB"
                        }
                        
                        notification_sent = self.notifications.send_notifications(rate_data)
                        
                        if notification_sent:
                            if current_rate < threshold:
                                self.logger.info("📧 Alert notification sent!")
                            else:
                                self.logger.info("📧 Daily summary sent!")
                        else:
                            self.logger.info("📧 No notification needed")
                    else:
                        self.logger.error("❌ Failed to fetch current exchange rate")
                    
                    self.logger.info(f"⏳ Waiting {interval} minutes before next check...")
                    time.sleep(interval * 60)
                    
                except Exception as e:
                    self.logger.error(f"❌ Error during monitoring cycle: {e}")
                    self.logger.info("⏳ Waiting 5 minutes before retry...")
                    time.sleep(300)  # Wait 5 minutes before retry
                    
        except KeyboardInterrupt:
            self.logger.info("🛑 Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Fatal error: {e}")


def main():
    """Main entry point for CAD-RMB Currency Bot"""
    print("💱 CAD-RMB Currency Exchange Rate Monitor 💱")
    print("=" * 50)
    
    bot = CADRMBCurrencyBot()
    
    # Check if running in non-interactive mode (e.g., Docker or daemon)
    is_docker = os.getenv("IS_DOCKER", "false").lower() == "true"
    force_interactive = os.getenv("FORCE_INTERACTIVE", "false").lower() == "true"
    is_daemon = os.getenv("CAD_RMB_MONITORING_INTERVAL") is not None
    
    if (is_docker or is_daemon) and not force_interactive:
        mode = "Docker" if is_docker else "Daemon"
        bot.logger.info(f"🐳 Running in non-interactive mode ({mode})")
        bot.run_continuous_monitoring()
        return
    
    # Interactive mode
    while True:
        print("\n📋 Choose monitoring mode:")
        print("1. Single rate check")
        print("2. Continuous monitoring")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            bot.run_single_check()
        elif choice == "2":
            bot.run_continuous_monitoring()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
