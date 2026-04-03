#!/usr/bin/env python3
"""
Trading Assistant Configuration
Technical analysis toolkit configuration.

Security: API keys are read from standard environment variables ONLY.
No .env file loading, no config file for secrets.
"""

from pathlib import Path
import os

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Data and log directories
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Technical analysis parameters (can be overridden via environment variables)
DEFAULT_CONFIG = {
    # Support/Resistance
    "support_resistance": {
        "lookback_days": int(os.environ.get("LOOKBACK_DAYS", "60")),
        "min_touches": int(os.environ.get("MIN_TOUCHES", "2")),
        "tolerance_pct": float(os.environ.get("SR_TOLERANCE_PCT", "1.0"))
    },
    
    # Trading signals
    "trading_signals": {
        "rsi_period": int(os.environ.get("RSI_PERIOD", "14")),
        "rsi_oversold": int(os.environ.get("RSI_OVERSOLD", "30")),
        "rsi_overbought": int(os.environ.get("RSI_OVERBOUGHT", "70")),
        "macd_fast": int(os.environ.get("MACD_FAST", "12")),
        "macd_slow": int(os.environ.get("MACD_SLOW", "26")),
        "macd_signal": int(os.environ.get("MACD_SIGNAL", "9")),
        "ma_short": int(os.environ.get("MA_SHORT", "20")),
        "ma_long": int(os.environ.get("MA_LONG", "50"))
    },
    
    # Position sizing
    "position_sizing": {
        "default_risk_pct": float(os.environ.get("DEFAULT_RISK_PCT", "2.0")),
        "max_position_pct": float(os.environ.get("MAX_POSITION_PCT", "20.0"))
    }
}

def get_api_key(provider):
    """Get API key from standard environment variables.
    
    Security: Only reads from standard environment variables.
    No .env file loading, no config file for secrets.
    
    Args:
        provider: API provider name ('twelve_data', 'alpha_vantage')
    
    Returns:
        str: API Key or None
    """
    provider = provider.upper()
    
    if provider in ["TWELVE_DATA", "TWELVE"]:
        return os.environ.get("TWELVE_DATA_API_KEY")
    elif provider in ["ALPHA_VANTAGE", "ALPHA", "AV"]:
        return os.environ.get("ALPHA_VANTAGE_API_KEY")
    else:
        return os.environ.get(f"{provider}_API_KEY")

def check_api_keys():
    """Check if required API keys are available.
    
    Returns:
        dict: {'twelve_data': bool, 'alpha_vantage': bool}
    """
    return {
        'twelve_data': os.environ.get("TWELVE_DATA_API_KEY") is not None,
        'alpha_vantage': os.environ.get("ALPHA_VANTAGE_API_KEY") is not None
    }

def get_config():
    """Get technical analysis configuration.
    
    Returns:
        dict: Configuration parameters
    """
    return DEFAULT_CONFIG.copy()

if __name__ == "__main__":
    print("🔧 Trading Assistant Configuration Test")
    print("=" * 60)
    
    api_status = check_api_keys()
    print(f"🔑 Twelve Data API Key: {'✅' if api_status['twelve_data'] else '❌'}")
    print(f"🔑 Alpha Vantage API Key: {'✅' if api_status['alpha_vantage'] else '❌ (optional)'}")
    print(f"📁 Data directory: {DATA_DIR}")
    print(f"📝 Log directory: {LOG_DIR}")
    print("=" * 60)
