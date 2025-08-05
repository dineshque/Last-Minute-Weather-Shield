import os
import io
import requests
from flask import Flask, request, jsonify, send_file, render_template
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
if not OPENWEATHERMAP_API_KEY:
    raise RuntimeError("Please set OPENWEATHERMAP_API_KEY in .env file")

# Actionable advice templates in Hindi and English for each risk type
ACTION_ADVICE = {
    'wind': {
        'hi': "Kal {value} km/hr hawa ke chances hain. Fasal dhak dijiye ya bamboo se support lagaiye.",
        'en': "Winds of {value} km/hr are expected tomorrow. Cover your crops or support them with bamboo."
    },
    'rain': {
        'hi': "Kal tez barish ke asaar hain (barish: {value} mm). Fasal ki naliyon ki safai kar lijiye.",
        'en': "Heavy rain is expected tomorrow ({value} mm). Clean crop drainage channels."
    },
    'hail': {
        'hi': "Kal ole padne ki sambhavna hai. Fasal ko cover karen ya bamboo/se support lagayen.",
        'en': "Hail is possible tomorrow. Cover your crops or use bamboo for protection."
    }
}

def detect_risks(weather_json):
    """Detect risky weather conditions in API response JSON."""
    risks = []
    # Wind risk threshold: over 40 km/h
    wind_speed = weather_json.get('wind', {}).get('speed', 0)
    if wind_speed > 40:
        risks.append({'type': 'wind', 'value': int(wind_speed)})

    # Rain risk threshold: more than 20 mm rain in last 1 or 3 hours 
    rain = weather_json.get('rain', {}).get('1h') or weather_json.get('rain', {}).get('3h') or 0
    if rain > 20:
        risks.append({'type': 'rain', 'value': rain})

    # Hail risk: check weather conditions for hail description or code 906
    for condition in weather_json.get('weather', []):
        if 'hail' in condition.get('description', '').lower() or condition.get('id') == 906:
            risks.append({'type': 'hail', 'value': True})

    return risks

def generate_advice(risks, lang='hi'):
    """Generate list of actionable advice strings based on risks detected."""
    advices = []
    for r in risks:
        adv_template = ACTION_ADVICE.get(r['type'], {}).get(lang)
        if adv_template:
            # Using format; hail doesn't use 'value', so safe to ignore missing keys
            try:
                msg = adv_template.format(**r)
            except KeyError:
                msg = adv_template
            advices.append(msg)
    return advices

@app.route('/')
def index():
    """Render the demo frontend page."""
    return render_template('index.html')

@app.route('/demo')
def demo():
    """Demo route to input city, get advice and play audio via frontend."""
    city = request.args.get('city')
    advice_hi = ''
    advice_en = ''
    error = ''
    if city:
        try:
            # Call internal weather endpoint to reuse code & logic
            res = requests.get(f'http://localhost:5000/weather?city={city}')
            data = res.json()
            if res.status_code == 200:
                # Join advisories as one string
                advice_hi = ' '.join(data.get('advice_hi', []))
                advice_en = ' '.join(data.get('advice_en', []))
                if not advice_hi:
                    error = "No actionable advice found for current weather."
            else:
                error = data.get('error', 'Error fetching weather data.')
        except Exception as e:
            error = f"Error fetching weather data: {str(e)}"
    else:
        error = 'City is required!'
    return render_template('index.html', advice_hi=advice_hi, advice_en=advice_en, error=error)

@app.route('/weather')
def get_weather():
    """Fetch weather data from OpenWeatherMap API, detect risks, generate advice."""
    city = request.args.get('city')
    lang = request.args.get('lang', 'hi')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    )
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Detect weather risks
        risks = detect_risks(data)
        data['risks'] = risks

        # Generate advice in both languages
        data['advice_hi'] = generate_advice(risks, lang='hi')
        data['advice_en'] = generate_advice(risks, lang='en')

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Could not fetch weather', 'details': str(e)}), 500

@app.route('/voice_alert', methods=['POST'])
def voice_alert():
    """Convert advice text message to speech and return audio (mp3)."""
    data = request.get_json(force=True)
    advice = data.get('message')
    lang = data.get('lang', 'hi')  # Default to Hindi

    if not advice or not isinstance(advice, str):
        return jsonify({'error': 'Valid "message" string is required'}), 400

    try:
        tts = gTTS(text=advice, lang=lang)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return send_file(mp3_fp, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': 'Failed to generate speech', 'details': str(e)}), 500

@app.route('/get_voice')
def get_voice():
    """Generate voice audio from advice message passed as query parameters."""
    message = request.args.get('message')
    lang = request.args.get('lang', 'hi')
    if not message:
        return 'No message provided', 400
    try:
        tts = gTTS(text=message, lang=lang)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return send_file(mp3_fp, mimetype='audio/mpeg')
    except Exception as e:
        return f"Error generating audio: {str(e)}", 500


if __name__ == '__main__':
    # Run Flask app in debug mode
    app.run(debug=True)
