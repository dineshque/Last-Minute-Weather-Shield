import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load env vars from .env

app = Flask(__name__)

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

@app.route('/weather')
def get_weather():
    # Get city from query parameter (e.g., /weather?city=Delhi)
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    # Build OpenWeatherMap API URL
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    )
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # Handle error with API call or invalid city
        return jsonify({'error': 'Could not fetch weather', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
