import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pyttsx3
import threading
from typing import Dict, List, Tuple

# Configuration
WEATHER_API_KEY = "your_openweathermap_api_key_here"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5"

# Language configurations
LANGUAGES = {
    'english': {'name': 'English', 'code': 'en'},
    'hindi': {'name': 'हिंदी', 'code': 'hi'},
    'punjabi': {'name': 'ਪੰਜਾਬੀ', 'code': 'pa'},
    'gujarati': {'name': 'ગુજરાતી', 'code': 'gu'},
    'marathi': {'name': 'मराठी', 'code': 'mr'},
    'tamil': {'name': 'தமிழ்', 'code': 'ta'},
    'telugu': {'name': 'తెలుగు', 'code': 'te'},
    'bengali': {'name': 'বাংলা', 'code': 'bn'},
    'kannada': {'name': 'ಕನ್ನಡ', 'code': 'kn'}
}

# UI Text translations
UI_TEXT = {
    'title': {
        'english': '🌾 Last-Minute Weather Shield - Crop-Saving Alerts',
        'hindi': '🌾 अंतिम समय मौसम सुरक्षा - फसल बचाने वाले अलर्ट',
        'punjabi': '🌾 ਆਖਰੀ ਸਮੇਂ ਮੌਸਮ ਸੁਰੱਖਿਆ - ਫਸਲ ਬਚਾਉਣ ਵਾਲੇ ਅਲਰਟ',
        'gujarati': '🌾 છેલ્લી ઘડીની હવામાન સુરક્ષા - પાક બચાવવાના અલર્ટ',
        'marathi': '🌾 शेवटच्या क्षणी हवामान संरक्षण - पीक वाचवणारे अलर्ट',
        'tamil': '🌾 கடைசி நிமிட வானிலை பாதுகாப்பு - பயிர் காக்கும் எச்சரிக்கைகள்',
        'telugu': '🌾 చివరి నిమిషం వాతావరణ రక్షణ - పంట రక్షణ హెచ్చరికలు',
        'bengali': '🌾 শেষ মুহূর্তের আবহাওয়া সুরক্ষা - ফসল রক্ষাকারী সতর্কতা',
        'kannada': '🌾 ಕೊನೆಯ ನಿಮಿಷದ ಹವಾಮಾನ ರಕ್ಷಣೆ - ಬೆಳೆ ರಕ್ಷಣಾ ಎಚ್ಚರಿಕೆಗಳು'
    },
    'subtitle': {
        'english': '*Weather alerts and action suggestions for crop protection*',
        'hindi': '*फसल सुरक्षा के लिए मौसम अलर्ट और कार्य सुझाव*',
        'punjabi': '*ਫਸਲ ਸੁਰੱਖਿਆ ਲਈ ਮੌਸਮ ਅਲਰਟ ਅਤੇ ਕਾਰਵਾਈ ਸੁਝਾਅ*',
        'gujarati': '*પાક સુરક્ષા માટે હવામાન અલર્ટ અને કાર્ય સૂચનો*',
        'marathi': '*पीक संरक्षणासाठी हवामान अलर्ट आणि कृती सूचना*',
        'tamil': '*பயிர் பாதுகாப்பிற்கான வானிலை எச்சரிக்கைகள் மற்றும் செயல் பரிந்துரைகள்*',
        'telugu': '*పంట రక్షణ కోసం వాతావరణ హెచ్చరికలు మరియు చర్య సూచనలు*',
        'bengali': '*ফসল সুরক্ষার জন্য আবহাওয়া সতর্কতা এবং কর্ম পরামর্শ*',
        'kannada': '*ಬೆಳೆ ರಕ್ಷಣೆಗಾಗಿ ಹವಾಮಾನ ಎಚ್ಚರಿಕೆಗಳು ಮತ್ತು ಕ್ರಿಯಾ ಸಲಹೆಗಳು*'
    },
    'settings': {
        'english': 'Settings',
        'hindi': 'सेटिंग्स',
        'punjabi': 'ਸੈਟਿੰਗਜ਼',
        'gujarati': 'સેટિંગ્સ',
        'marathi': 'सेटिंग्स',
        'tamil': 'அமைப்புகள்',
        'telugu': 'సెట్టింగులు',
        'bengali': 'সেটিংস',
        'kannada': 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು'
    },
    'enter_city': {
        'english': 'Enter your city:',
        'hindi': 'अपना शहर दर्ज करें:',
        'punjabi': 'ਆਪਣਾ ਸ਼ਹਿਰ ਦਾਖਲ ਕਰੋ:',
        'gujarati': 'તમારું શહેર દાખલ કરો:',
        'marathi': 'तुमचे शहर प्रविष्ट करा:',
        'tamil': 'உங்கள் நகரத்தை உள்ளிடவும்:',
        'telugu': 'మీ నగరాన్ని నమోదు చేయండి:',
        'bengali': 'আপনার শহর লিখুন:',
        'kannada': 'ನಿಮ್ಮ ನಗರವನ್ನು ನಮೂದಿಸಿ:'
    },
    'language_select': {
        'english': 'Language / भाषा / ਭਾਸ਼ਾ',
        'hindi': 'भाषा / Language / ਭਾਸ਼ਾ',
        'punjabi': 'ਭਾਸ਼ਾ / Language / भाषा',
        'gujarati': 'ભાષા / Language / भाषा',
        'marathi': 'भाषा / Language / ਭਾਸ਼ਾ',
        'tamil': 'மொழி / Language / भाषा',
        'telugu': 'భాష / Language / भाषा',
        'bengali': 'ভাষা / Language / भाषा',
        'kannada': 'ಭಾಷೆ / Language / भाषा'
    },
    'voice_alerts': {
        'english': 'Enable Voice Alerts',
        'hindi': 'आवाज़ अलर्ट सक्षम करें',
        'punjabi': 'ਆਵਾਜ਼ ਅਲਰਟ ਸਮਰੱਥ ਕਰੋ',
        'gujarati': 'અવાજ અલર્ટ સક્ષમ કરો',
        'marathi': 'आवाज अलर्ट सक्षम करा',
        'tamil': 'குரல் எச்சரிக்கைகளை இயக்கவும்',
        'telugu': 'వాయిస్ అలర్ట్‌లను ప్రారంభించండి',
        'bengali': 'ভয়েস অ্যালার্ট সক্ষম করুন',
        'kannada': 'ಧ್ವನಿ ಎಚ್ಚರಿಕೆಗಳನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ'
    },
    'get_forecast': {
        'english': '🌤️ Get Weather Forecast',
        'hindi': '🌤️ मौसम पूर्वानुमान प्राप्त करें',
        'punjabi': '🌤️ ਮੌਸਮ ਪੂਰਵ ਅਨੁਮਾਨ ਪ੍ਰਾਪਤ ਕਰੋ',
        'gujarati': '🌤️ હવામાન આગાહી મેળવો',
        'marathi': '🌤️ हवामान अंदाज मिळवा',
        'tamil': '🌤️ வானிலை முன்னறிவிப்பு பெறுங்கள்',
        'telugu': '🌤️ వాతావరణ సూచన పొందండి',
        'bengali': '🌤️ আবহাওয়ার পূর্বাভাস পান',
        'kannada': '🌤️ ಹವಾಮಾನ ಮುನ್ನೋಟ ಪಡೆಯಿರಿ'
    },
    'current_weather': {
        'english': '🌡️ Current Weather',
        'hindi': '🌡️ वर्तमान मौसम',
        'punjabi': '🌡️ ਮੌਜੂਦਾ ਮੌਸਮ',
        'gujarati': '🌡️ વર્તમાન હવામાન',
        'marathi': '🌡️ सध्याचे हवामान',
        'tamil': '🌡️ தற்போதைய வானிலை',
        'telugu': '🌡️ ప్రస్తుత వాతావరణం',
        'bengali': '🌡️ বর্তমান আবহাওয়া',
        'kannada': '🌡️ ಪ್ರಸ್ತುತ ಹವಾಮಾನ'
    },
    'crop_risk_analysis': {
        'english': '⚠️ Crop Risk Analysis',
        'hindi': '⚠️ फसल जोखिम विश्लेषण',
        'punjabi': '⚠️ ਫਸਲ ਜੋਖਮ ਵਿਸ਼ਲੇਸ਼ਣ',
        'gujarati': '⚠️ પાક જોખમ વિશ્લેષણ',
        'marathi': '⚠️ पीक जोखीम विश्लेषण',
        'tamil': '⚠️ பயிர் ஆபத்து பகுப்பாய்வு',
        'telugu': '⚠️ పంట ప్రమాద విశ్లేషణ',
        'bengali': '⚠️ ফসল ঝুঁকি বিশ্লেষণ',
        'kannada': '⚠️ ಬೆಳೆ ಅಪಾಯ ವಿಶ್ಲೇಷಣೆ'
    },
    'no_risks': {
        'english': '✅ No immediate crop risks detected!',
        'hindi': '✅ कोई तत्काल फसल जोखिम नहीं मिला!',
        'punjabi': '✅ ਕੋਈ ਤੁਰੰਤ ਫਸਲ ਜੋਖਮ ਨਹੀਂ ਮਿਲਿਆ!',
        'gujarati': '✅ કોઈ તાત્કાલિક પાક જોખમ મળ્યું નથી!',
        'marathi': '✅ कोणताही तात्काळ पीक धोका आढळला नाही!',
        'tamil': '✅ உடனடி பயிர் ஆபத்துகள் எதுவும் கண்டறியப்படவில்லை!',
        'telugu': '✅ తక్షణ పంట ప్రమాదాలు ఏవీ గుర్తించబడలేదు!',
        'bengali': '✅ কোনো তাৎক্ষণিক ফসল ঝুঁকি শনাক্ত হয়নি!',
        'kannada': '✅ ಯಾವುದೇ ತಕ್ಷಣದ ಬೆಳೆ ಅಪಾಯಗಳು ಪತ್ತೆಯಾಗಿಲ್ಲ!'
    },
    'forecast_chart': {
        'english': '📊 3-Day Weather Forecast',
        'hindi': '📊 3-दिन का मौसम पूर्वानुमान',
        'punjabi': '📊 3-ਦਿਨ ਦਾ ਮੌਸਮ ਪੂਰਵ ਅਨੁਮਾਨ',
        'gujarati': '📊 3-દિવસની હવામાન આગાહી',
        'marathi': '📊 3-दिवसांचा हवामान अंदाज',
        'tamil': '📊 3-நாள் வானிலை முன்னறிவிப்பு',
        'telugu': '📊 3-రోజుల వాతావరణ సూచన',
        'bengali': '📊 3-দিনের আবহাওয়ার পূর্বাভাস',
        'kannada': '📊 3-ದಿನಗಳ ಹವಾಮಾನ ಮುನ್ನೋಟ'
    },
    'detailed_forecast': {
        'english': '📅 Detailed Forecast',
        'hindi': '📅 विस्तृत पूर्वानुमान',
        'punjabi': '📅 ਵਿਸਤ੍ਰਿਤ ਪੂਰਵ ਅਨੁਮਾਨ',
        'gujarati': '📅 વિગતવાર આગાહી',
        'marathi': '📅 तपशीलवार अंदाज',
        'tamil': '📅 விரிவான முன்னறிவிப்பு',
        'telugu': '📅 వివరణాత్మక సూచన',
        'bengali': '📅 বিস্তারিত পূর্বাভাস',
        'kannada': '📅 ವಿವರವಾದ ಮುನ್ನೋಟ'
    },
    'error_city': {
        'english': 'Please enter a city name',
        'hindi': 'कृपया शहर का नाम दर्ज करें',
        'punjabi': 'ਕਿਰਪਾ ਕਰਕੇ ਸ਼ਹਿਰ ਦਾ ਨਾਮ ਦਾਖਲ ਕਰੋ',
        'gujarati': 'કૃપા કરીને શહેરનું નામ દાખલ કરો',
        'marathi': 'कृपया शहराचे नाव प्रविष्ट करा',
        'tamil': 'தயவுசெய்து நகரத்தின் பெயரை உள்ளிடவும்',
        'telugu': 'దయచేసి నగర పేరును నమోదు చేయండి',
        'bengali': 'অনুগ্রহ করে শহরের নাম লিখুন',
        'kannada': 'ದಯವಿಟ್ಟು ನಗರದ ಹೆಸರನ್ನು ನಮೂದಿಸಿ'
    },
    'error_api': {
        'english': 'Please add your OpenWeatherMap API key in the code',
        'hindi': 'कृपया कोड में अपनी OpenWeatherMap API key जोड़ें',
        'punjabi': 'ਕਿਰਪਾ ਕਰਕੇ ਕੋਡ ਵਿੱਚ ਆਪਣੀ OpenWeatherMap API key ਸ਼ਾਮਲ ਕਰੋ',
        'gujarati': 'કૃપા કરીને કોડમાં તમારી OpenWeatherMap API key ઉમેરો',
        'marathi': 'कृपया कोडमध्ये तुमची OpenWeatherMap API key जोडा',
        'tamil': 'தயவுசெய்து குறியீட்டில் உங்கள் OpenWeatherMap API key ஐ சேர்க்கவும்',
        'telugu': 'దయచేసి కోడ్‌లో మీ OpenWeatherMap API key ని జోడించండి',
        'bengali': 'অনুগ্রহ করে কোডে আপনার OpenWeatherMap API key যোগ করুন',
        'kannada': 'ದಯವಿಟ್ಟು ಕೋಡ್‌ನಲ್ಲಿ ನಿಮ್ಮ OpenWeatherMap API key ಅನ್ನು ಸೇರಿಸಿ'
    },
    'fetching_data': {
        'english': 'Fetching weather data...',
        'hindi': 'मौसम डेटा प्राप्त कर रहे हैं...',
        'punjabi': 'ਮੌਸਮ ਡੇਟਾ ਪ੍ਰਾਪਤ ਕਰ ਰਹੇ ਹਾਂ...',
        'gujarati': 'હવામાન ડેટા મેળવી રહ્યા છીએ...',
        'marathi': 'हवामान डेटा मिळवत आहे...',
        'tamil': 'வானிலை தரவுகளைப் பெறுகிறது...',
        'telugu': 'వాతావరణ డేటాను పొందుతోంది...',
        'bengali': 'আবহাওয়ার তথ্য সংগ্রহ করা হচ্ছে...',
        'kannada': 'ಹವಾಮಾನ ಡೇಟಾವನ್ನು ಪಡೆಯುತ್ತಿದೆ...'
    }
}

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_weather(self, city: str) -> Dict:
        """Get current weather data for a city"""
        url = f"{BASE_URL}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching current weather: {e}")
            return None

    def get_forecast(self, city: str, days: int = 3) -> Dict:
        """Get weather forecast for next few days"""
        url = f"{BASE_URL}/forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (every 3 hours)
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching forecast: {e}")
            return None

class CropAlertSystem:
    def __init__(self):
        self.risk_thresholds = {
            'wind_speed': 15,  # m/s (54 km/hr)
            'heavy_rain': 20,  # mm/hour
            'hail_keywords': ['hail', 'thunderstorm', 'severe'],
            'temperature_low': 5,  # Celsius
            'temperature_high': 45,  # Celsius
            'humidity_high': 90  # %
        }

        self.crop_actions = {
            'high_wind': {
                'english': "Provide bamboo or wooden support to crops due to high winds. Remove plastic mulch.",
                'hindi': "तेज़ हवा के कारण फसल को बांस या लकड़ी से सहारा दीजिये। प्लास्टिक मल्च हटाएं।",
                'punjabi': "ਤੇਜ਼ ਹਵਾ ਕਾਰਨ ਫਸਲ ਨੂੰ ਬਾਂਸ ਜਾਂ ਲੱਕੜ ਨਾਲ ਸਹਾਰਾ ਦਿਓ। ਪਲਾਸਟਿਕ ਮਲਚ ਹਟਾਓ।",
                'gujarati': "તેજ પવનને કારણે પાકને વાંસ અથવા લાકડાથી આધાર આપો। પ્લાસ્ટિક મલ્ચ હટાવો।",
                'marathi': "जोरदार वाऱ्यामुळे पिकाला बांबू किंवा लाकडाचा आधार द्या। प्लास्टिक मल्च काढा।",
                'tamil': "வலுவான காற்றால் பயிர்களுக்கு மூங்கில் அல்லது மரத்தால் ஆதரவு கொடுங்கள். பிளாஸ்டிக் மல்ச் அகற்றவும்।",
                'telugu': "బలమైన గాలుల వల్ల పంటలకు వెదురు లేదా కలపతో మద్దతు ఇవ్వండి. ప్లాస్టిక్ మల్చ్ తొలగించండి।",
                'bengali': "প্রবল বাতাসের কারণে ফসলকে বাঁশ বা কাঠ দিয়ে সাহায্য করুন। প্লাস্টিক মালচ সরান।",
                'kannada': "ಬಲವಾದ ಗಾಳಿಯಿಂದಾಗಿ ಬೆಳೆಗಳಿಗೆ ಬಿದಿರು ಅಥವಾ ಮರದಿಂದ ಬೆಂಬಲ ನೀಡಿ। ಪ್ಲಾಸ್ಟಿಕ್ ಮಲ್ಚ್ ತೆಗೆದುಹಾಕಿ।"
            },
            'heavy_rain': {
                'english': "Create proper drainage to prevent waterlogging. Cover crops if possible.",
                'hindi': "भारी बारिश से बचने के लिए जल निकासी बनाएं। फसल को ढकें।",
                'punjabi': "ਪਾਣੀ ਭਰਨ ਤੋਂ ਬਚਣ ਲਈ ਸਹੀ ਨਿਕਾਸ ਬਣਾਓ। ਫਸਲ ਨੂੰ ਢੱਕੋ।",
                'gujarati': "પાણી ભરાવાથી બચવા માટે યોગ્ય ડ્રેનેજ બનાવો। પાકને ઢાંકો।",
                'marathi': "पाणी साचण्यापासून वाचण्यासाठी योग्य निचरा तयार करा। पिकांना झाकून ठेवा।",
                'tamil': "நீர் தேங்குவதைத் தடுக்க சரியான வடிகால் அமைக்கவும். பயிர்களை மூடவும்।",
                'telugu': "నీరు నిలిచిపోకుండా సరైన డ్రైనేజీ చేయండి. పంటలను కప్పండి।",
                'bengali': "জল জমা রোধ করতে সঠিক নিকাশি ব্যবস্থা করুন। ফসল ঢেকে রাখুন।",
                'kannada': "ನೀರು ನಿಲ್ಲುವುದನ್ನು ತಡೆಯಲು ಸರಿಯಾದ ಒಳಚರಂಡಿ ಮಾಡಿ। ಬೆಳೆಗಳನ್ನು ಮುಚ್ಚಿ।"
            },
            'hail_risk': {
                'english': "Hail risk detected! Cover crops immediately with nets or tarpaulin.",
                'hindi': "ओले पड़ने का खतरा है! फसल को तुरंत जाल या तिरपाल से ढक दीजिये।",
                'punjabi': "ਗੜੇ ਪੈਣ ਦਾ ਖ਼ਤਰਾ ਹੈ! ਫਸਲ ਨੂੰ ਤੁਰੰਤ ਜਾਲ ਜਾਂ ਤਿਰਪਾਲ ਨਾਲ ਢੱਕੋ।",
                'gujarati': "કરા પડવાનું જોખમ છે! પાકને તુરંત જાળી અથવા તિરપાલથી ઢાંકો।",
                'marathi': "गारपीट पडण्याचा धोका आहे! पिकांना ताबडतोब जाळी किंवा तिरपालने झाकून टाका।",
                'tamil': "கல்மழை ஆபத்து! பயிர்களை உடனே வலை அல்லது தார்ப்பாலினால் மூடுங்கள்।",
                'telugu': "వడగళ్ళు పడే ప్రమాదం! పంటలను వెంటనే వలలు లేదా తార్పాలిన్‌తో కప్పండి।",
                'bengali': "শিলাবৃষ্টির ঝুঁকি! ফসল তৎক্ষণাৎ জাল বা তেরপল দিয়ে ঢেকে দিন।",
                'kannada': "ಆಲಿಕಲ್ಲು ಅಪಾಯ! ಬೆಳೆಗಳನ್ನು ತಕ್ಷಣ ಬಲೆ ಅಥವಾ ತಾರ್ಪಾಲಿನ್‌ನಿಂದ ಮುಚ್ಚಿ।"
            },
            'frost_risk': {
                'english': "Frost risk detected. Keep crops warm with smoke or heaters.",
                'hindi': "पाला पड़ने का डर है। फसल को धुआं या हीटर से गर्म रखें।",
                'punjabi': "ਪਾਲਾ ਪੈਣ ਦਾ ਡਰ ਹੈ। ਫਸਲ ਨੂੰ ਧੂੰਆਂ ਜਾਂ ਹੀਟਰ ਨਾਲ ਗਰਮ ਰੱਖੋ।",
                'gujarati': "હિમ પડવાનું જોખમ છે. પાકને ધુમાડા અથવા હીટરથી ગરમ રાખો।",
                'marathi': "दंव पडण्याचा धोका आहे. पिकांना धूर किंवा हीटरने उबदार ठेवा।",
                'tamil': "உறைபனி ஆபத்து கண்டறியப்பட்டது. பயிர்களை புகை அல்லது ஹீட்டர் மூலம் சூடாக வைக்கவும்.",
                'telugu': "మంచు ప్రమాదం గుర్తించబడింది. పంటలను పొగ లేదా హీటర్‌తో వేడిగా ఉంచండి।",
                'bengali': "তুষারপাতের ঝুঁকি শনাক্ত হয়েছে। ধোঁয়া বা হিটার দিয়ে ফসল গরম রাখুন।",
                'kannada': "ಹಿಮ ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ. ಹೊಗೆ ಅಥವಾ ಹೀಟರ್‌ನಿಂದ ಬೆಳೆಗಳನ್ನು ಬೆಚ್ಚಗಾಗಿಸಿ."
            },
            'heat_wave': {
                'english': "Extreme heat detected. Use shade nets and increase irrigation.",
                'hindi': "बहुत गर्मी है। फसल को छाया जाल लगाएं और ज्यादा पानी दें।",
                'punjabi': "ਬਹੁਤ ਗਰਮੀ ਹੈ। ਫਸਲ ਨੂੰ ਛਾਂ ਦੇ ਜਾਲ ਲਗਾਓ ਅਤੇ ਜ਼ਿਆਦਾ ਪਾਣੀ ਦਿਓ।",
                'gujarati': "અતિશય ગરમી છે. પાક પર છાયાની જાળી લગાવો અને વધુ પાણી આપો.",
                'marathi': "अतिशय उष्णता आहे. पिकांवर सावलीचे जाळे लावा आणि जास्त पाणी द्या।",
                'tamil': "கடுமையான வெப்பம் கண்டறியப்பட்டது. நிழல் வலைகளைப் பயன்படுத்தி நீர்ப்பாசனத்தை அதிகரிக்கவும்.",
                'telugu': "తీవ్రమైన వేడిమి గుర్తించబడింది. నీడ వలలను ఉపయోగించి నీటిపారుదలను పెంచండి।",
                'bengali': "প্রচণ্ড গরম শনাক্ত হয়েছে। ছায়ার জাল ব্যবহার করুন এবং সেচ বাড়ান।",
                'kannada': "ತೀವ್ರ ಶಾಖ ಪತ್ತೆಯಾಗಿದೆ. ನೆರಳು ಬಲೆಗಳನ್ನು ಬಳಸಿ ಮತ್ತು ನೀರಾವರಿ ಹೆಚ್ಚಿಸಿ."
            }
        }

    def analyze_weather_risks(self, weather_data: Dict) -> List[Dict]:
        """Analyze weather data and identify crop risks"""
        risks = []

        if not weather_data:
            return risks

        # Current weather analysis
        if 'main' in weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']

            if temp <= self.risk_thresholds['temperature_low']:
                risks.append({
                    'type': 'frost_risk',
                    'severity': 'high',
                    'message': self.crop_actions['frost_risk']
                })

            if temp >= self.risk_thresholds['temperature_high']:
                risks.append({
                    'type': 'heat_wave',
                    'severity': 'high',
                    'message': self.crop_actions['heat_wave']
                })

        if 'wind' in weather_data:
            wind_speed = weather_data['wind']['speed']
            if wind_speed >= self.risk_thresholds['wind_speed']:
                risks.append({
                    'type': 'high_wind',
                    'severity': 'medium',
                    'message': self.crop_actions['high_wind']
                })

        if 'weather' in weather_data:
            weather_desc = weather_data['weather'][0]['description'].lower()
            for keyword in self.risk_thresholds['hail_keywords']:
                if keyword in weather_desc:
                    risks.append({
                        'type': 'hail_risk',
                        'severity': 'critical',
                        'message': self.crop_actions['hail_risk']
                    })
                    break

        return risks

    def analyze_forecast_risks(self, forecast_data: Dict) -> List[Dict]:
        """Analyze forecast data for upcoming risks"""
        risks = []

        if not forecast_data or 'list' not in forecast_data:
            return risks

        for forecast in forecast_data['list'][:24]:  # Next 3 days (8 forecasts per day)
            dt = datetime.fromtimestamp(forecast['dt'])

            # Check for heavy rain
            if 'rain' in forecast and '3h' in forecast['rain']:
                rain_3h = forecast['rain']['3h']
                if rain_3h > self.risk_thresholds['heavy_rain']:
                    risks.append({
                        'type': 'heavy_rain',
                        'severity': 'high',
                        'time': dt.strftime('%Y-%m-%d %H:%M'),
                        'message': self.crop_actions['heavy_rain']
                    })

            # Check weather conditions
            weather_desc = forecast['weather'][0]['description'].lower()
            for keyword in self.risk_thresholds['hail_keywords']:
                if keyword in weather_desc:
                    risks.append({
                        'type': 'hail_risk',
                        'severity': 'critical',
                        'time': dt.strftime('%Y-%m-%d %H:%M'),
                        'message': self.crop_actions['hail_risk']
                    })
                    break

        return risks

class VoiceAlert:
    def __init__(self):
        self.engine = None
        self.initialize_tts()

    def initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            # Set properties
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level
        except Exception as e:
            st.warning(f"Voice alert system not available: {e}")

    def speak_alert(self, message: str, language: str = 'hindi'):
        """Speak the alert message"""
        if not self.engine:
            return

        def speak():
            try:
                self.engine.say(message)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Error in voice alert: {e}")

        # Run in separate thread to avoid blocking
        thread = threading.Thread(target=speak)
        thread.daemon = True
        thread.start()

def create_weather_chart(forecast_data: Dict) -> go.Figure:
    """Create weather forecast visualization"""
    if not forecast_data or 'list' not in forecast_data:
        return None

    dates = []
    temps = []
    humidity = []
    wind_speeds = []
    rain = []

    for forecast in forecast_data['list'][:24]:  # Next 3 days
        dt = datetime.fromtimestamp(forecast['dt'])
        dates.append(dt)
        temps.append(forecast['main']['temp'])
        humidity.append(forecast['main']['humidity'])
        wind_speeds.append(forecast['wind']['speed'] * 3.6)  # Convert to km/h

        rain_val = 0
        if 'rain' in forecast and '3h' in forecast['rain']:
            rain_val = forecast['rain']['3h']
        rain.append(rain_val)

    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Temperature (°C)', 'Humidity (%)', 'Wind Speed (km/h)', 'Rainfall (mm)'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )

    # Temperature
    fig.add_trace(
        go.Scatter(x=dates, y=temps, mode='lines+markers', name='Temperature', line=dict(color='red')),
        row=1, col=1
    )

    # Humidity
    fig.add_trace(
        go.Scatter(x=dates, y=humidity, mode='lines+markers', name='Humidity', line=dict(color='blue')),
        row=1, col=2
    )

    # Wind Speed
    fig.add_trace(
        go.Scatter(x=dates, y=wind_speeds, mode='lines+markers', name='Wind Speed', line=dict(color='green')),
        row=2, col=1
    )

    # Rainfall
    fig.add_trace(
        go.Bar(x=dates, y=rain, name='Rainfall', marker_color='lightblue'),
        row=2, col=2
    )

    fig.update_layout(height=600, showlegend=False, title_text="3-Day Weather Forecast")
    return fig

def main():
    st.set_page_config(
        page_title="Crop Weather Shield",
        page_icon="🌾",
        layout="wide"
    )

    # Initialize services
    weather_service = WeatherService(WEATHER_API_KEY)
    alert_system = CropAlertSystem()
    voice_alert = VoiceAlert()

    # Sidebar for settings
    st.sidebar.header("Settings")
    city = st.sidebar.text_input("Enter your city:", value="Delhi")

    # Language selection with native names
    language_options = {lang_data['name']: lang_key for lang_key, lang_data in LANGUAGES.items()}
    selected_language_name = st.sidebar.selectbox(
        "Language / भाषा / ਭਾਸ਼ਾ / ભાષા / भाषा / மொழி / భాష / ভাষা / ಭಾಷೆ:",
        list(language_options.keys())
    )
    language = language_options[selected_language_name]

    voice_enabled = st.sidebar.checkbox(UI_TEXT['voice_alerts'][language], value=True)

    # Dynamic title and subtitle based on selected language
    st.title(UI_TEXT['title'][language])
    st.markdown(UI_TEXT['subtitle'][language])

    # Main weather forecasting button
    if st.button(UI_TEXT['get_forecast'][language], type="primary", use_container_width=True):
        if not city:
            st.error(UI_TEXT['error_city'][language])
            return

        if WEATHER_API_KEY == "your_openweathermap_api_key_here":
            st.error(UI_TEXT['error_api'][language])
            return

        with st.spinner(UI_TEXT['fetching_data'][language]):
            # Get current weather
            current_weather = weather_service.get_current_weather(city)
            forecast_data = weather_service.get_forecast(city, days=3)

            if current_weather and forecast_data:
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.subheader(UI_TEXT['current_weather'][language])
                    temp = current_weather['main']['temp']
                    feels_like = current_weather['main']['feels_like']
                    humidity = current_weather['main']['humidity']
                    wind_speed = current_weather['wind']['speed'] * 3.6  # Convert to km/h
                    description = current_weather['weather'][0]['description'].title()

                    st.metric("Temperature", f"{temp}°C", f"Feels like {feels_like}°C")
                    st.metric("Humidity", f"{humidity}%")
                    st.metric("Wind Speed", f"{wind_speed:.1f} km/h")
                    st.info(f"Condition: {description}")

                with col2:
                    st.subheader(UI_TEXT['crop_risk_analysis'][language])

                    # Analyze current risks
                    current_risks = alert_system.analyze_weather_risks(current_weather)
                    forecast_risks = alert_system.analyze_forecast_risks(forecast_data)

                    all_risks = current_risks + forecast_risks

                    if all_risks:
                        for risk in all_risks:
                            severity_color = {
                                'critical': '🔴',
                                'high': '🟠',
                                'medium': '🟡'
                            }.get(risk['severity'], '🟢')

                            message = risk['message'][language]
                            st.warning(f"{severity_color} **{risk['type'].replace('_', ' ').title()}**\n\n{message}")

                            # Voice alert for critical risks
                            if voice_enabled and risk['severity'] == 'critical':
                                voice_alert.speak_alert(message, language)
                    else:
                        st.success(UI_TEXT['no_risks'][language])

                # Weather forecast chart
                st.subheader(UI_TEXT['forecast_chart'][language])
                chart = create_weather_chart(forecast_data)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)

                # Detailed forecast table
                st.subheader(UI_TEXT['detailed_forecast'][language])
                forecast_df = []
                for forecast in forecast_data['list'][:24]:
                    dt = datetime.fromtimestamp(forecast['dt'])
                    forecast_df.append({
                        'Date': dt.strftime('%Y-%m-%d'),
                        'Time': dt.strftime('%H:%M'),
                        'Temperature (°C)': forecast['main']['temp'],
                        'Humidity (%)': forecast['main']['humidity'],
                        'Wind Speed (km/h)': round(forecast['wind']['speed'] * 3.6, 1),
                        'Condition': forecast['weather'][0]['description'].title()
                    })

                df = pd.DataFrame(forecast_df)
                st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()