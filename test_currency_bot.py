#!/usr/bin/env python3
"""
Test script for Currency Exchange Rate Monitor
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from currency.config.currency_config import CurrencyConfig
from currency.monitor.currency_monitor import CurrencyMonitor
from currency.notifications.currency_notifications import CurrencyNotificationManager


def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    config = CurrencyConfig()
    
    # Test API config
    api_config = config.get_api_config()
    print(f"API URL: {api_config['api_url']}")
    print(f"Base Currency: {api_config['base_currency']}")
    print(f"Target Currency: {api_config['target_currency']}")
    
    # Test monitoring config
    monitoring_config = config.get_monitoring_config()
    print(f"Monitoring Interval: {monitoring_config['monitoring_interval']} minutes")
    print(f"Threshold: {monitoring_config['threshold']}")
    
    print("✅ Configuration test passed")
    return True


def test_monitor():
    """Test currency monitoring"""
    print("\nTesting currency monitoring...")
    config = CurrencyConfig()
    monitor = CurrencyMonitor(config)
    
    # Test getting current rate
    rate = monitor.get_current_rate()
    if rate:
        print(f"Current RMB-CAD rate: {rate}")
        print("✅ Currency monitoring test passed")
        return True
    else:
        print("❌ Failed to get exchange rate")
        return False


def test_notifications():
    """Test notification system"""
    print("\nTesting notification system...")
    config = CurrencyConfig()
    notifications = CurrencyNotificationManager(config)
    
    # Test email formatting
    test_data = {
        "current_rate": 5.02,
        "threshold": 5.05,
        "timestamp": "2025-01-27T10:00:00",
        "currency_pair": "RMB-CAD"
    }
    
    email_body = notifications._format_email_message(test_data)
    if email_body and "5.02" in email_body:
        print("✅ Email formatting test passed")
        return True
    else:
        print("❌ Email formatting test failed")
        return False


def main():
    """Run all tests"""
    print("🧪 Currency Exchange Rate Monitor - Test Suite")
    print("=" * 50)
    
    tests = [
        test_config,
        test_monitor,
        test_notifications
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The currency bot is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
