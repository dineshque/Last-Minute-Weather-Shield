import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load env vars from .env

app = Flask(__name__)

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    url = (f"http://api.openweathermap.org/data/2.5/weather"
           f"?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Risk detection logic!
        risks = detect_risks(data)
        data['risks'] = risks
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Could not fetch weather', 'details': str(e)}), 500

def detect_risks(weather_json):
    risks = []
    # Wind risk
    wind_speed = weather_json.get('wind', {}).get('speed', 0)
    if wind_speed > 40:
        risks.append({'type': 'wind', 'value': wind_speed})

    # Rain risk
    rain = weather_json.get('rain', {}).get('1h') or weather_json.get('rain', {}).get('3h') or 0
    if rain > 20:
        risks.append({'type': 'rain', 'value': rain})

    # Hail risk: check weather condition
    for condition in weather_json.get('weather', []):
        if 'hail' in condition.get('description', '').lower() or condition.get('id') == 906:
            risks.append({'type': 'hail', 'value': True})

    return risks


if __name__ == '__main__':
    app.run(debug=True)
