# 🌾 Last-Minute Weather Shield - Crop-Saving Alerts

A smart weather forecasting system that provides actionable crop-saving alerts in Hindi and English. The system detects risky weather conditions like hailstorms, high winds, heavy rain, and extreme temperatures, then provides specific actions farmers can take to protect their crops.

## Features

- **Real-time Weather Data**: Uses OpenWeatherMap API for accurate weather information
- **Crop Risk Analysis**: Intelligent analysis of weather conditions that can damage crops
- **Actionable Alerts**: Specific instructions on what actions to take (not just weather info)
- **Multilingual Support**: Alerts in 9 Indian languages + English
- **Voice Alerts**: Text-to-speech for critical warnings
- **3-Day Forecast**: Weather predictions with interactive charts
- **Demo Mode**: Test the app without API key using sample data

## Risk Detection

The system detects and alerts for:
- **High Winds** (>54 km/hr): Suggests bamboo support, removing plastic mulch
- **Heavy Rain**: Recommends drainage creation, crop covering
- **Hail Risk**: Critical alerts to cover crops immediately
- **Frost Risk**: Suggests warming methods (smoke, heaters)
- **Heat Waves**: Recommends shade nets, increased irrigation

## Supported Languages

The system supports **10 languages** with native script support:

- 🇬🇧 **English** - Complete interface and alerts
- 🇮🇳 **हिंदी (Hindi)** - पूर्ण इंटरफेस और अलर्ट
- 🇮🇳 **ਪੰਜਾਬੀ (Punjabi)** - ਪੂਰਾ ਇੰਟਰਫੇਸ ਅਤੇ ਅਲਰਟ
- 🇮🇳 **ગુજરાતી (Gujarati)** - સંપૂર્ણ ઇન્ટરફેસ અને અલર્ટ
- 🇮🇳 **मराठी (Marathi)** - संपूर्ण इंटरफेस आणि अलर्ट
- 🇮🇳 **தமிழ் (Tamil)** - முழு இடைமுகம் மற்றும் எச்சரிக்கைகள்
- 🇮🇳 **తెలుగు (Telugu)** - పూర్తి ఇంటర్‌ఫేస్ మరియు హెచ్చరికలు
- 🇮🇳 **বাংলা (Bengali)** - সম্পূর্ণ ইন্টারফেস এবং সতর্কতা
- 🇮🇳 **ಕನ್ನಡ (Kannada)** - ಸಂಪೂರ್ಣ ಇಂಟರ್‌ಫೇಸ್ ಮತ್ತು ಎಚ್ಚರಿಕೆಗಳು

## Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
python setup.py
```

This will:
- Check Python version compatibility
- Install all dependencies
- Help you set up the API key
- Test the installation
- Show usage instructions

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Get OpenWeatherMap API Key**
   - Go to [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key from the dashboard
   - Replace `"your_openweathermap_api_key_here"` in `app.py` with your actual API key

3. **Run the Application**

**For real weather data:**
```bash
streamlit run app.py
```

**For demo with sample data:**
```bash
streamlit run demo_app.py
```

## Usage

1. **Enter your city** in the sidebar
2. **Select language** from 10 supported languages
3. **Enable voice alerts** if desired
4. **Click "Get Weather Forecast"** button
5. **Review current weather** and crop risk analysis
6. **Check 3-day forecast** charts and detailed table
7. **Take recommended actions** for any detected risks

## Example Multilingual Alerts

### English:
- "Provide bamboo or wooden support to crops due to high winds"
- "Hail risk detected! Cover crops immediately with nets or tarpaulin"
- "Create proper drainage to prevent waterlogging"

### Hindi (हिंदी):
- "तेज़ हवा के कारण फसल को बांस या लकड़ी से सहारा दीजिये"
- "ओले पड़ने का खतरा है! फसल को तुरंत जाल या तिरपाल से ढक दीजिये"
- "भारी बारिश से बचने के लिए जल निकासी बनाएं"

### Punjabi (ਪੰਜਾਬੀ):
- "ਤੇਜ਼ ਹਵਾ ਕਾਰਨ ਫਸਲ ਨੂੰ ਬਾਂਸ ਜਾਂ ਲੱਕੜ ਨਾਲ ਸਹਾਰਾ ਦਿਓ"
- "ਗੜੇ ਪੈਣ ਦਾ ਖ਼ਤਰਾ ਹੈ! ਫਸਲ ਨੂੰ ਤੁਰੰਤ ਜਾਲ ਜਾਂ ਤਿਰਪਾਲ ਨਾਲ ਢੱਕੋ"

### Tamil (தமிழ்):
- "வலுவான காற்றால் பயிர்களுக்கு மூங்கில் அல்லது மரத்தால் ஆதரவு கொடுங்கள்"
- "கல்மழை ஆபத்து! பயிர்களை உடனே வலை அல்லது தார்ப்பாலினால் மூடுங்கள்"

### Telugu (తెలుగు):
- "బలమైన గాలుల వల్ల పంటలకు వెదురు లేదా కలపతో మద్దతు ఇవ్వండి"
- "వడగళ్ళు పడే ప్రమాదం! పంటలను వెంటనే వలలు లేదా తార్పాలిన్‌తో కప్పండి"

## File Structure

```
├── app.py              # Main application with real weather data
├── demo_app.py         # Demo version with sample data
├── config.py           # Configuration and multilingual settings
├── setup.py            # Automated setup script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Configuration

You can customize risk thresholds and crop-specific actions in `config.py`:

- Wind speed thresholds
- Temperature limits
- Rainfall amounts
- Crop-specific recommendations

## Dependencies

- **streamlit**: Web app framework
- **requests**: HTTP requests for weather API
- **pandas**: Data manipulation
- **plotly**: Interactive charts
- **pyttsx3**: Text-to-speech for voice alerts

## API Information

This app uses the OpenWeatherMap API:
- **Current Weather**: `/weather` endpoint
- **5-Day Forecast**: `/forecast` endpoint (3-hour intervals)
- **Free Tier**: 1000 calls/day, sufficient for personal use

## Troubleshooting

### Common Issues:

1. **"Import could not be resolved"**: Install dependencies with `pip install -r requirements.txt`

2. **"API key error"**: Make sure you've replaced the placeholder API key with your actual key

3. **"Voice alerts not working"**: pyttsx3 might not be available on your system. The app will work without voice alerts.

4. **"No weather data"**: Check your internet connection and API key validity

### Testing Without API Key:

Use the demo version to test functionality:
```bash
streamlit run demo_app.py
```

## Future Enhancements

- SMS/WhatsApp integration for alerts
- Crop-specific recommendations based on growth stage
- Historical weather pattern analysis
- Integration with soil moisture sensors
- Multi-location monitoring for large farms

## Contributing

Feel free to contribute by:
- Adding more crop-specific actions
- Improving risk detection algorithms
- Adding support for more languages
- Enhancing the user interface

## License

This project is open source and available under the MIT License.
