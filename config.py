"""
Configuration file for Weather Shield App
"""

import os
from typing import Optional

def get_weather_api_key() -> Optional[str]:
    """
    Get OpenWeatherMap API key from environment variable or return None
    
    To set up:
    1. Go to https://openweathermap.org/api
    2. Sign up for a free account
    3. Get your API key
    4. Set environment variable: OPENWEATHER_API_KEY=your_key_here
    
    Or modify the WEATHER_API_KEY in app.py directly
    """
    return os.getenv('OPENWEATHER_API_KEY')

# Weather thresholds for crop alerts (can be customized)
CROP_RISK_THRESHOLDS = {
    'wind_speed_ms': 15,  # m/s (54 km/hr)
    'heavy_rain_mm': 20,  # mm per 3 hours
    'temperature_low_c': 5,  # Celsius
    'temperature_high_c': 45,  # Celsius
    'humidity_high_percent': 90  # %
}

# Multilingual crop-specific actions
CROP_ACTIONS = {
    'wheat': {
        'high_wind': {
            'english': "Support wheat crops with bamboo stakes. Remove plastic mulch.",
            'hindi': "गेहूं की फसल को बांस से सहारा दें। प्लास्टिक मल्च हटाएं।",
            'punjabi': "ਕਣਕ ਦੀ ਫਸਲ ਨੂੰ ਬਾਂਸ ਨਾਲ ਸਹਾਰਾ ਦਿਓ। ਪਲਾਸਟਿਕ ਮਲਚ ਹਟਾਓ।",
            'gujarati': "ઘઉંના પાકને વાંસથી આધાર આપો. પ્લાસ્ટિક મલ્ચ હટાવો.",
            'marathi': "गहूच्या पिकाला बांबूने आधार द्या. प्लास्टिक मल्च काढा.",
            'tamil': "கோதுமை பயிர்களுக்கு மூங்கில் ஆதரவு கொடுங்கள். பிளாஸ்டிக் மல்ச் அகற்றவும்.",
            'telugu': "గోధుమ పంటలకు వెదురుతో మద్దతు ఇవ్వండి। ప్లాస్టిక్ మల్చ్ తొలగించండి।",
            'bengali': "গমের ফসলকে বাঁশ দিয়ে সাহায্য করুন। প্লাস্টিক মালচ সরান।",
            'kannada': "ಗೋಧಿ ಬೆಳೆಗಳಿಗೆ ಬಿದಿರಿನಿಂದ ಬೆಂಬಲ ನೀಡಿ। ಪ್ಲಾಸ್ಟಿಕ್ ಮಲ್ಚ್ ತೆಗೆದುಹಾಕಿ।"
        },
        'heavy_rain': {
            'english': "Create drainage in wheat fields. Apply fungicide spray.",
            'hindi': "गेहूं के खेत में पानी का निकास बनाएं। फंगीसाइड स्प्रे करें।",
            'punjabi': "ਕਣਕ ਦੇ ਖੇਤ ਵਿੱਚ ਪਾਣੀ ਦਾ ਨਿਕਾਸ ਬਣਾਓ। ਫੰਗੀਸਾਈਡ ਸਪ੍ਰੇ ਕਰੋ।",
            'gujarati': "ઘઉંના ખેતરમાં ડ્રેનેજ બનાવો. ફંગીસાઈડ સ્પ્રે કરો.",
            'marathi': "गहूच्या शेतात निचरा तयार करा. बुरशीनाशक फवारणी करा.",
            'tamil': "கோதுமை வயல்களில் வடிகால் அமைக்கவும். பூஞ்சைக் கொல்லி தெளிக்கவும்.",
            'telugu': "గోధుమ పొలాల్లో డ్రైనేజీ చేయండి. ఫంగిసైడ్ స్ప్రే చేయండి।",
            'bengali': "গমের ক্ষেতে নিকাশি ব্যবস্থা করুন। ছত্রাকনাশক স্প্রে করুন।",
            'kannada': "ಗೋಧಿ ಹೊಲಗಳಲ್ಲಿ ಒಳಚರಂಡಿ ಮಾಡಿ। ಶಿಲೀಂಧ್ರನಾಶಕ ಸಿಂಪಡಿಸಿ।"
        }
    },
    'rice': {
        'high_wind': {
            'english': "Support rice crops. Reduce water level in fields.",
            'hindi': "धान की फसल को सहारा दें। खेत में पानी का स्तर कम करें।",
            'punjabi': "ਧਾਨ ਦੀ ਫਸਲ ਨੂੰ ਸਹਾਰਾ ਦਿਓ। ਖੇਤ ਵਿੱਚ ਪਾਣੀ ਦਾ ਪੱਧਰ ਘਟਾਓ।",
            'gujarati': "ચોખાના પાકને આધાર આપો. ખેતરમાં પાણીનું સ્તર ઘટાડો.",
            'marathi': "भाताच्या पिकाला आधार द्या. शेतात पाण्याची पातळी कमी करा.",
            'tamil': "நெல் பயிர்களுக்கு ஆதரவு கொடுங்கள். வயல்களில் நீர் மட்டத்தை குறைக்கவும்.",
            'telugu': "వరి పంటలకు మద్దతు ఇవ్వండి. పొలాల్లో నీటి మట్టాన్ని తగ్గించండి।",
            'bengali': "ধানের ফসলকে সাহায্য করুন। ক্ষেতে পানির স্তর কমান।",
            'kannada': "ಅಕ್ಕಿ ಬೆಳೆಗಳಿಗೆ ಬೆಂಬಲ ನೀಡಿ। ಹೊಲಗಳಲ್ಲಿ ನೀರಿನ ಮಟ್ಟವನ್ನು ಕಡಿಮೆ ಮಾಡಿ।"
        },
        'heavy_rain': {
            'english': "Ensure proper drainage in rice fields.",
            'hindi': "धान के खेत में अतिरिक्त पानी का निकास करें।",
            'punjabi': "ਧਾਨ ਦੇ ਖੇਤ ਵਿੱਚ ਵਾਧੂ ਪਾਣੀ ਦਾ ਨਿਕਾਸ ਕਰੋ।",
            'gujarati': "ચોખાના ખેતરમાં યોગ્ય ડ્રેનેજ સુનિશ્ચિત કરો.",
            'marathi': "भाताच्या शेतात योग्य निचरा सुनिश्चित करा.",
            'tamil': "நெல் வயல்களில் சரியான வடிகால் உறுதி செய்யவும்.",
            'telugu': "వరి పొలాల్లో సరైన డ్రైనేజీని నిర్ధారించండి।",
            'bengali': "ধানের ক্ষেতে সঠিক নিকাশি নিশ্চিত করুন।",
            'kannada': "ಅಕ್ಕಿ ಹೊಲಗಳಲ್ಲಿ ಸರಿಯಾದ ಒಳಚರಂಡಿ ಖಚಿತಪಡಿಸಿ।"
        }
    },
    'vegetables': {
        'high_wind': {
            'english': "Cover vegetables with nets. Provide support structures.",
            'hindi': "सब्जियों को जाल से ढकें। सहारे की संरचना प्रदान करें।",
            'punjabi': "ਸਬਜ਼ੀਆਂ ਨੂੰ ਜਾਲ ਨਾਲ ਢੱਕੋ। ਸਹਾਰੇ ਦੀ ਬਣਤਰ ਪ੍ਰਦਾਨ ਕਰੋ।",
            'gujarati': "શાકભાજીને જાળીથી ઢાંકો. આધારની રચના પ્રદાન કરો.",
            'marathi': "भाज्यांना जाळ्याने झाकून टाका. आधाराची रचना प्रदान करा.",
            'tamil': "காய்கறிகளை வலையால் மூடவும். ஆதரவு கட்டமைப்புகளை வழங்கவும்.",
            'telugu': "కూరగాయలను వలలతో కప్పండి. మద్దతు నిర్మాణాలను అందించండి।",
            'bengali': "সবজি জাল দিয়ে ঢেকে দিন। সহায়ক কাঠামো প্রদান করুন।",
            'kannada': "ತರಕಾರಿಗಳನ್ನು ಬಲೆಗಳಿಂದ ಮುಚ್ಚಿ। ಬೆಂಬಲ ರಚನೆಗಳನ್ನು ಒದಗಿಸಿ।"
        },
        'hail_risk': {
            'english': "Cover vegetables immediately with tarpaulin!",
            'hindi': "सब्जियों को तुरंत तिरपाल से ढक दें!",
            'punjabi': "ਸਬਜ਼ੀਆਂ ਨੂੰ ਤੁਰੰਤ ਤਿਰਪਾਲ ਨਾਲ ਢੱਕੋ!",
            'gujarati': "શાકભાજીને તુરંત તિરપાલથી ઢાંકો!",
            'marathi': "भाज्यांना ताबडतोब तिरपालने झाकून टाका!",
            'tamil': "காய்கறிகளை உடனே தார்ப்பாலினால் மூடுங்கள்!",
            'telugu': "కూరగాయలను వెంటనే తార్పాలిన్‌తో కప్పండి!",
            'bengali': "সবজি তৎক্ষণাৎ তেরপল দিয়ে ঢেকে দিন!",
            'kannada': "ತರಕಾರಿಗಳನ್ನು ತಕ್ಷಣ ತಾರ್ಪಾಲಿನ್‌ನಿಂದ ಮುಚ್ಚಿ!"
        }
    }
}

# Cities with their coordinates (for better weather accuracy)
MAJOR_CITIES = {
    'Delhi': {'lat': 28.6139, 'lon': 77.2090},
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
    'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
    'Chennai': {'lat': 13.0827, 'lon': 80.2707},
    'Kolkata': {'lat': 22.5726, 'lon': 88.3639},
    'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
    'Pune': {'lat': 18.5204, 'lon': 73.8567},
    'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714},
    'Jaipur': {'lat': 26.9124, 'lon': 75.7873},
    'Lucknow': {'lat': 26.8467, 'lon': 80.9462}
}
