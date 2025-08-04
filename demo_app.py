import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import time

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
        'english': '🌾 Last-Minute Weather Shield - Demo Version',
        'hindi': '🌾 अंतिम समय मौसम सुरक्षा - डेमो संस्करण',
        'punjabi': '🌾 ਆਖਰੀ ਸਮੇਂ ਮੌਸਮ ਸੁਰੱਖਿਆ - ਡੈਮੋ ਸੰਸਕਰਣ',
        'gujarati': '🌾 છેલ્લી ઘડીની હવામાન સુરક્ષા - ડેમો વર્ઝન',
        'marathi': '🌾 शेवटच्या क्षणी हवामान संरक्षण - डेमो आवृत्ती',
        'tamil': '🌾 கடைசி நிமிட வானிலை பாதுகாப்பு - டெமோ பதிப்பு',
        'telugu': '🌾 చివరి నిమిషం వాతావరణ రక్షణ - డెమో వెర్షన్',
        'bengali': '🌾 শেষ মুহূর্তের আবহাওয়া সুরক্ষা - ডেমো সংস্করণ',
        'kannada': '🌾 ಕೊನೆಯ ನಿಮಿಷದ ಹವಾಮಾನ ರಕ್ಷಣೆ - ಡೆಮೋ ಆವೃತ್ತಿ'
    },
    'subtitle': {
        'english': '*Weather alerts and action suggestions for crop protection (Demo with sample data)*',
        'hindi': '*फसल सुरक्षा के लिए मौसम अलर्ट और कार्य सुझाव (नमूना डेटा के साथ डेमो)*',
        'punjabi': '*ਫਸਲ ਸੁਰੱਖਿਆ ਲਈ ਮੌਸਮ ਅਲਰਟ ਅਤੇ ਕਾਰਵਾਈ ਸੁਝਾਅ (ਨਮੂਨਾ ਡੇਟਾ ਨਾਲ ਡੈਮੋ)*',
        'gujarati': '*પાક સુરક્ષા માટે હવામાન અલર્ટ અને કાર્ય સૂચનો (નમૂના ડેટા સાથે ડેમો)*',
        'marathi': '*पीक संरक्षणासाठी हवामान अलर्ट आणि कृती सूचना (नमुना डेटासह डेमो)*',
        'tamil': '*பயிர் பாதுகாப்பிற்கான வானிலை எச்சரிக்கைகள் மற்றும் செயல் பரிந்துரைகள் (மாதிரி தரவுகளுடன் டெமோ)*',
        'telugu': '*పంట రక్షణ కోసం వాతావరణ హెచ్చరికలు మరియు చర్య సూచనలు (నమూనా డేటాతో డెమో)*',
        'bengali': '*ফসল সুরক্ষার জন্য আবহাওয়া সতর্কতা এবং কর্ম পরামর্শ (নমুনা ডেটা সহ ডেমো)*',
        'kannada': '*ಬೆಳೆ ರಕ್ಷಣೆಗಾಗಿ ಹವಾಮಾನ ಎಚ್ಚರಿಕೆಗಳು ಮತ್ತು ಕ್ರಿಯಾ ಸಲಹೆಗಳು (ಮಾದರಿ ಡೇಟಾದೊಂದಿಗೆ ಡೆಮೋ)*'
    },
    'demo_info': {
        'english': '🔔 This is a demo version using sample weather data. For real weather data, use the main app with OpenWeatherMap API key.',
        'hindi': '🔔 यह नमूना मौसम डेटा का उपयोग करने वाला डेमो संस्करण है। वास्तविक मौसम डेटा के लिए, OpenWeatherMap API key के साथ मुख्य ऐप का उपयोग करें।',
        'punjabi': '🔔 ਇਹ ਨਮੂਨਾ ਮੌਸਮ ਡੇਟਾ ਦੀ ਵਰਤੋਂ ਕਰਨ ਵਾਲਾ ਡੈਮੋ ਸੰਸਕਰਣ ਹੈ। ਅਸਲ ਮੌਸਮ ਡੇਟਾ ਲਈ, OpenWeatherMap API key ਨਾਲ ਮੁੱਖ ਐਪ ਦੀ ਵਰਤੋਂ ਕਰੋ।',
        'gujarati': '🔔 આ નમૂના હવામાન ડેટાનો ઉપયોગ કરતું ડેમો વર્ઝન છે. વાસ્તવિક હવામાન ડેટા માટે, OpenWeatherMap API key સાથે મુખ્ય એપ્લિકેશનનો ઉપયોગ કરો.',
        'marathi': '🔔 हे नमुना हवामान डेटा वापरणारी डेमो आवृत्ती आहे. वास्तविक हवामान डेटासाठी, OpenWeatherMap API key सह मुख्य अॅप वापरा.',
        'tamil': '🔔 இது மாதிரி வானிலை தரவுகளைப் பயன்படுத்தும் டெமோ பதிப்பு. உண்மையான வானிலை தரவுகளுக்கு, OpenWeatherMap API key உடன் முக்கிய பயன்பாட்டைப் பயன்படுத்தவும்.',
        'telugu': '🔔 ఇది నమూనా వాతావరణ డేటాను ఉపయోగించే డెమో వెర్షన్. నిజమైన వాతావరణ డేటా కోసం, OpenWeatherMap API key తో ప్రధాన యాప్‌ను ఉపయోగించండి.',
        'bengali': '🔔 এটি নমুনা আবহাওয়ার তথ্য ব্যবহার করে একটি ডেমো সংস্করণ। প্রকৃত আবহাওয়ার তথ্যের জন্য, OpenWeatherMap API key সহ মূল অ্যাপ ব্যবহার করুন।',
        'kannada': '🔔 ಇದು ಮಾದರಿ ಹವಾಮಾನ ಡೇಟಾವನ್ನು ಬಳಸುವ ಡೆಮೋ ಆವೃತ್ತಿ. ನಿಜವಾದ ಹವಾಮಾನ ಡೇಟಾಗಾಗಿ, OpenWeatherMap API key ಯೊಂದಿಗೆ ಮುಖ್ಯ ಅಪ್ಲಿಕೇಶನ್ ಅನ್ನು ಬಳಸಿ.'
    },
    'get_forecast_demo': {
        'english': '🌤️ Get Weather Forecast (Demo)',
        'hindi': '🌤️ मौसम पूर्वानुमान प्राप्त करें (डेमो)',
        'punjabi': '🌤️ ਮੌਸਮ ਪੂਰਵ ਅਨੁਮਾਨ ਪ੍ਰਾਪਤ ਕਰੋ (ਡੈਮੋ)',
        'gujarati': '🌤️ હવામાન આગાહી મેળવો (ડેમો)',
        'marathi': '🌤️ हवामान अंदाज मिळवा (डेमो)',
        'tamil': '🌤️ வானிலை முன்னறிவிப்பு பெறுங்கள் (டெமோ)',
        'telugu': '🌤️ వాతావరణ సూచన పొందండి (డెమో)',
        'bengali': '🌤️ আবহাওয়ার পূর্বাভাস পান (ডেমো)',
        'kannada': '🌤️ ಹವಾಮಾನ ಮುನ್ನೋಟ ಪಡೆಯಿರಿ (ಡೆಮೋ)'
    }
}

# Demo data generator
def generate_demo_weather_data():
    """Generate realistic demo weather data"""
    current_time = datetime.now()
    
    # Current weather
    current_weather = {
        'main': {
            'temp': random.uniform(15, 35),
            'feels_like': random.uniform(15, 35),
            'humidity': random.randint(40, 90)
        },
        'wind': {
            'speed': random.uniform(2, 20)  # m/s
        },
        'weather': [{
            'description': random.choice(['clear sky', 'few clouds', 'scattered clouds', 
                                        'broken clouds', 'shower rain', 'rain', 
                                        'thunderstorm', 'snow', 'mist'])
        }]
    }
    
    # Forecast data
    forecast_data = {'list': []}
    for i in range(24):  # 3 days, 8 forecasts per day
        forecast_time = current_time + timedelta(hours=i*3)
        forecast = {
            'dt': int(forecast_time.timestamp()),
            'main': {
                'temp': random.uniform(10, 40),
                'humidity': random.randint(30, 95)
            },
            'wind': {
                'speed': random.uniform(1, 25)
            },
            'weather': [{
                'description': random.choice(['clear sky', 'few clouds', 'scattered clouds',
                                            'broken clouds', 'shower rain', 'rain',
                                            'thunderstorm', 'snow', 'mist'])
            }]
        }
        
        # Add rain data randomly
        if random.random() < 0.3:  # 30% chance of rain
            forecast['rain'] = {'3h': random.uniform(0.5, 25)}
        
        forecast_data['list'].append(forecast)
    
    return current_weather, forecast_data

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
                'telugu': "బలమైన గాలుల వల్ల పంటలకు వెదురు లేదా కలపతో మద్దతు ఇవ్వండి। ప్లాస్టిక్ మల్చ్ తొలగించండి।",
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
                'telugu': "నీరు నిలిచిపోకుండా సరైన డ్రైనేజీ చేయండి। పంటలను కప్పండి।",
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
                'tamil': "உறைபனி ஆபத்து கண்டறியப்பட்டது. பயிர்களை புகை அல்லது ஹீட்டர் மூலம் சூடாக வைக்கவும்।",
                'telugu': "మంచు ప్రమాదం గుర్తించబడింది. పంటలను పొగ లేదా హీటర్‌తో వేడిగా ఉంచండి।",
                'bengali': "তুষারপাতের ঝুঁকি শনাক্ত হয়েছে। ধোঁয়া বা হিটার দিয়ে ফসল গরম রাখুন।",
                'kannada': "ಹಿಮ ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ. ಹೊಗೆ ಅಥವಾ ಹೀಟರ್‌ನಿಂದ ಬೆಳೆಗಳನ್ನು ಬೆಚ್ಚಗಾಗಿಸಿ।"
            },
            'heat_wave': {
                'english': "Extreme heat detected. Use shade nets and increase irrigation.",
                'hindi': "बहुत गर्मी है। फसल को छाया जाल लगाएं और ज्यादा पानी दें।",
                'punjabi': "ਬਹੁਤ ਗਰਮੀ ਹੈ। ਫਸਲ ਨੂੰ ਛਾਂ ਦੇ ਜਾਲ ਲਗਾਓ ਅਤੇ ਜ਼ਿਆਦਾ ਪਾਣੀ ਦਿਓ।",
                'gujarati': "અતિશય ગરમી છે. પાક પર છાયાની જાળી લગાવો અને વધુ પાણી આપો।",
                'marathi': "अतिशय उष्णता आहे. पिकांवर सावलीचे जाळे लावा आणि जास्त पाणी द्या।",
                'tamil': "கடுமையான வெப்பம் கண்டறியப்பட்டது. நிழல் வலைகளைப் பயன்படுத்தி நீர்ப்பாசனத்தை அதிகரிக்கவும்।",
                'telugu': "తీవ్రమైన వేడిమి గుర్తించబడింది. నీడ వలలను ఉపయోగించి నీటిపారుదలను పెంచండి।",
                'bengali': "প্রচণ্ড গরম শনাক্ত হয়েছে। ছায়ার জাল ব্যবহার করুন এবং সেচ বাড়ান।",
                'kannada': "ತೀವ್ರ ಶಾಖ ಪತ್ತೆಯಾಗಿದೆ. ನೆರಳು ಬಲೆಗಳನ್ನು ಬಳಸಿ ಮತ್ತು ನೀರಾವರಿ ಹೆಚ್ಚಿಸಿ।"
            }
        }
    
    def analyze_weather_risks(self, weather_data):
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
    
    def analyze_forecast_risks(self, forecast_data):
        """Analyze forecast data for upcoming risks"""
        risks = []
        
        if not forecast_data or 'list' not in forecast_data:
            return risks
        
        for forecast in forecast_data['list'][:24]:  # Next 3 days
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

def create_weather_chart(forecast_data):
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
    
    fig.update_layout(height=600, showlegend=False, title_text="3-Day Weather Forecast (Demo Data)")
    return fig

def main():
    st.set_page_config(
        page_title="Crop Weather Shield - Demo",
        page_icon="🌾",
        layout="wide"
    )

    # Initialize alert system
    alert_system = CropAlertSystem()

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

    # Dynamic title and subtitle based on selected language
    st.title(UI_TEXT['title'][language])
    st.markdown(UI_TEXT['subtitle'][language])

    st.info(UI_TEXT['demo_info'][language])
    
    # Main weather forecasting button
    if st.button(UI_TEXT['get_forecast_demo'][language], type="primary", use_container_width=True):
        with st.spinner("Generating demo weather data..."):
            time.sleep(1)  # Simulate API call delay
            
            # Generate demo data
            current_weather, forecast_data = generate_demo_weather_data()
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("🌡️ Current Weather (Demo)")
                temp = current_weather['main']['temp']
                feels_like = current_weather['main']['feels_like']
                humidity = current_weather['main']['humidity']
                wind_speed = current_weather['wind']['speed'] * 3.6  # Convert to km/h
                description = current_weather['weather'][0]['description'].title()
                
                st.metric("Temperature", f"{temp:.1f}°C", f"Feels like {feels_like:.1f}°C")
                st.metric("Humidity", f"{humidity}%")
                st.metric("Wind Speed", f"{wind_speed:.1f} km/h")
                st.info(f"Condition: {description}")
            
            with col2:
                st.subheader("⚠️ Crop Risk Analysis")
                
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
                else:
                    st.success("✅ No immediate crop risks detected!")
            
            # Weather forecast chart
            st.subheader("📊 3-Day Weather Forecast")
            chart = create_weather_chart(forecast_data)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            
            # Detailed forecast table
            st.subheader("📅 Detailed Forecast")
            forecast_df = []
            for forecast in forecast_data['list'][:24]:
                dt = datetime.fromtimestamp(forecast['dt'])
                forecast_df.append({
                    'Date': dt.strftime('%Y-%m-%d'),
                    'Time': dt.strftime('%H:%M'),
                    'Temperature (°C)': round(forecast['main']['temp'], 1),
                    'Humidity (%)': forecast['main']['humidity'],
                    'Wind Speed (km/h)': round(forecast['wind']['speed'] * 3.6, 1),
                    'Condition': forecast['weather'][0]['description'].title()
                })
            
            df = pd.DataFrame(forecast_df)
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
