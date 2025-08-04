#!/usr/bin/env python3
"""
Setup script for Last-Minute Weather Shield
Helps users set up the application with proper dependencies and API key
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🌾 LAST-MINUTE WEATHER SHIELD SETUP")
    print("   Crop-Saving Weather Alert System")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("   Please run: pip install -r requirements.txt")
        return False

def setup_api_key():
    """Help user set up OpenWeatherMap API key"""
    print("\n🔑 API Key Setup")
    print("To get real weather data, you need a free OpenWeatherMap API key:")
    print("1. Go to: https://openweathermap.org/api")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    print()
    
    api_key = input("Enter your OpenWeatherMap API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Update the API key in app.py
        try:
            with open('app.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace(
                'WEATHER_API_KEY = "your_openweathermap_api_key_here"',
                f'WEATHER_API_KEY = "{api_key}"'
            )
            
            with open('app.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ API key saved to app.py")
            return True
        except Exception as e:
            print(f"❌ Error saving API key: {e}")
            return False
    else:
        print("⚠️  API key skipped. You can use the demo version or add it later.")
        return False

def test_installation():
    """Test if the installation works"""
    print("\n🧪 Testing installation...")
    
    try:
        import streamlit
        import requests
        import pandas
        import plotly
        print("✅ All required packages are available")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False

def show_usage_instructions(has_api_key):
    """Show how to run the application"""
    print("\n🚀 Usage Instructions")
    print("=" * 40)
    
    if has_api_key:
        print("To run with REAL weather data:")
        print("   streamlit run app.py")
        print()
    
    print("To run DEMO version (sample data):")
    print("   streamlit run demo_app.py")
    print()
    
    print("📱 Supported Languages:")
    languages = [
        "🇬🇧 English", "🇮🇳 हिंदी (Hindi)", "🇮🇳 ਪੰਜਾਬੀ (Punjabi)",
        "🇮🇳 ગુજરાતી (Gujarati)", "🇮🇳 मराठी (Marathi)", "🇮🇳 தமிழ் (Tamil)",
        "🇮🇳 తెలుగు (Telugu)", "🇮🇳 বাংলা (Bengali)", "🇮🇳 ಕನ್ನಡ (Kannada)"
    ]
    for lang in languages:
        print(f"   • {lang}")
    
    print("\n🌾 Features:")
    features = [
        "Real-time weather data with 3-day forecast",
        "Smart crop risk detection (wind, rain, hail, frost, heat)",
        "Actionable farming advice in your language",
        "Voice alerts for critical warnings",
        "Interactive weather charts and detailed forecasts"
    ]
    for feature in features:
        print(f"   • {feature}")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  You can still run the demo version if dependencies are installed manually")
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed. Please install missing packages.")
        sys.exit(1)
    
    # Setup API key
    has_api_key = setup_api_key()
    
    # Show usage instructions
    show_usage_instructions(has_api_key)
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete! Happy farming! 🌾")
    print("=" * 60)

if __name__ == "__main__":
    main()
